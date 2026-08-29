---
title: The Real Cost of a Single Inference Call
summary: What actually happens in memory when you run one forward pass on a 70B model — and where the numbers people quote come from.
date: August 25, 2026
tags:
  - llm
  - inference
  - pytorch
  - gpu
  - performance
draft: true
---

You've probably seen the claim that "a 70B model needs 140GB of VRAM." It's half right, and the missing half is exactly the part that determines whether your workload fits on a single GPU, a node, or a rack. This post walks through the memory layout of one inference call, layer by layer, so you can derive the number yourself instead of trusting a blog post — including this one.

We'll use a 70B-parameter transformer as the running example. The math generalizes; the specific numbers don't.

## Where the money actually goes

At inference time, four things live in GPU memory at once:

- **Model weights** — the parameters themselves, loaded once and shared across every request
- **KV cache** — per-sequence attention state, grows with context length and batch size
- **Activations** — intermediate tensors for the current forward pass, freed afterward
- **Workspace** — cuBLAS/cuDNN scratch buffers, fragmentation, allocator overhead

Let's size each one.

### Weights

In FP16 (or BF16), each parameter is 2 bytes. A 70B model:

```python
params = 70e9
bytes_per_param = 2  # fp16/bf16
weights_gb = params * bytes_per_param / 1e9
print(f"Weights: {weights_gb:.0f} GB")
```

That's the 140GB figure. In FP8 it drops to ~70GB; in INT4, roughly 35GB plus a non-trivial accuracy tax depending on the quantization scheme.

Note what this number does *not* include: the KV cache, the activations, or the workspace. It is a lower bound on what you need to even load the model, not a lower bound on what you need to serve it.

### KV cache: the part everyone underestimates

For every token in the sequence, each layer stores a key and a value vector. For a model with `L` layers, `h` attention heads, and head dimension `d_head`, the per-token KV size is `2 · L · h · d_head` elements (the factor of 2 for keys and values).

For a typical 70B-class architecture (`L=80`, `h=64`, `d_head=128`):

```python
L, h, d_head = 80, 64, 128
bytes_per_token = 2 * L * h * d_head * 2  # *2 for K and V, *2 bytes for fp16
seq_len = 8192
kv_cache_mb = bytes_per_token * seq_len / 1e6
print(f"KV cache per sequence: {kv_cache_mb:.0f} MB")
```

Scale that by your batch size and context length and you'll often find the KV cache, not the weights, is the binding constraint. This is why long-context serving is a fundamentally different problem from short-context serving, even for the same model.

### Activations

During the forward pass, each layer's intermediate tensors (attention scores, MLP intermediates) exist simultaneously. For a single sequence with batch 1, this is modest — a few GB at most for a 70B model. For training with gradient checkpointing off, it's a different story entirely; we'll touch on that contrast in the follow-up post on training memory.

### Workspace

cuBLAS and the CUDA allocator need headroom. Rule of thumb: budget 10–20% of your remaining VRAM as slack. The allocator's fragmentation behavior means you can be "within budget" on paper and still hit an OOM at runtime.

## Putting it together: the inference budget

For a single sequence, batch size 1, context length `S`, FP16:

```
Total ≈ Weights + KV(S) + Activations + Workspace
      ≈ 140 GB  + ~0.5 GB per 1k tokens + a few GB + headroom
```

A practical 8×H100 node (640GB) comfortably serves a 70B model at moderate context. A single H100 (80GB) cannot even load the FP16 weights — you need FP8, quantization, or tensor parallelism across multiple GPUs.

The two regimes:

| Regime | Dominant term | Scaling |
|--------|--------------|---------|
| Short context, large batch | Weights (amortized) | Throughput ↑ with batch until KV dominates |
| Long context, small batch | KV cache | Memory ↑ linearly with context length |

## Why this matters for how you build

Three practical consequences:

1. **Batch size is a memory decision, not just a throughput decision.** Every additional sequence in the batch adds `S × kv_per_token` to your footprint.
2. **Context length is a product decision with a direct hardware cost.** Doubling max context doubles KV memory.
3. **Quantization trades are asymmetric.** Weight quantization shrinks the static term; it does nothing for KV unless you also quantize the cache, which has its own accuracy implications.

## Related

- [PyTorch Mental Model](post/002-pytorch-mental-model.md) — how PyTorch's tensor model maps onto what we're sizing here
