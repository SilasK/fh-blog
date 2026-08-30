# fh-blog

A personal blog engine built with [FastHTML](https://fastht.ml) and [MonsterUI](https://monsterui.answer.ai). Write posts in Markdown (or Jupyter notebooks), run live Python code blocks in the browser, and serve everything from a single Python file.

[Use this template](https://github.com/SilasK/fh-blog) to create your own blog.

## Features

- **Dynamic Content**: Posts support live Python code execution (`python:run` code blocks)
- **Notebooks as Posts**: `.ipynb` files alongside `.md` files, same frontmatter
- **Modern UI**: Responsive design powered by MonsterUI
- **Tag Filtering**: Top-5 tag filter with HTMX (no page reload)
- **Configurable**: All site settings in one `config.yaml`
- **Single File App**: The entire server is `app.py`
- **Reproducible Env**: [Pixi](https://pixi.sh) for dependencies

## Getting Started

1. Create a new repository from this template (the "Use this template" button).
2. Clone it and install dependencies:

   ```bash
   git clone https://github.com/you/your-blog.git
   cd your-blog
   pixi install
   ```

3. Create your configuration:

   ```bash
   cp config.example.yaml config.yaml
   ```

   Then edit `config.yaml` with your title, subtitle, URL, social links, and theme.

4. Write a post: drop a Markdown file (or `.ipynb`) into `posts/`. Subfolders
   become URL prefixes — `posts/post/foo.md` is served at `/post/foo`,
   `posts/events/meetup.md` at `/events/meetup`.

   ```markdown
   ---
   title: My First Post
   summary: One sentence shown on the home page.
   date: January 1, 2026
   tags:
     - hello
   ---

   Hello world!
   ```

   Posts with `draft: true` in the frontmatter are hidden from the home page
   but still reachable by URL.

5. Run the dev server:

   ```bash
   pixi run dev
   ```

   The blog is at http://localhost:8001 with live-reload.

## Production

Run without live-reload:

```bash
pixi run start
```

(`dev` and `start` both run `python app.py`; `dev` sets `RELOAD=1`, which
enables file-watch reload and the live-reload client.)

To put it on a domain, run it on a machine with a public address and point a
reverse proxy or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
at `http://localhost:8001`. For example, a Cloudflare tunnel ingress route:

```yaml
ingress:
  - hostname: yourdomain.com
    service: http://localhost:8001
  - hostname: www.yourdomain.com
    service: http://localhost:8001
  - service: http_status:404
```

## Configuration

All site settings live in `config.yaml` (see `config.example.yaml` for the
annotated schema):

- **Blog settings**: title, subtitle, description, URL (used for Open Graph / Twitter Card meta tags)
- **Author information**: name, email, bio
- **Social media links**: GitHub, X, Bluesky, LinkedIn, Mastodon (each with a `display` flag)
- **SEO settings**: Twitter card image, favicon
- **Theme settings**: primary color, code highlight theme, supported languages
- **Display settings**: posts per page, tags, comments, analytics

## Linking Between Posts

Link to another post by its **file path** instead of a full URL — the blog
resolves it to the real post URL at render time:

```markdown
[Getting Started](post/getting-started.md)
[An Event](events/meetup.md)
```

External URLs (`https://...`) automatically open in a new tab; internal post
links stay in the same tab.

## Technology Stack

- **FastHTML**: Python web framework (server + templates in one language)
- **MonsterUI**: UI components and styling (Tailwind-based)
- **fh-posts**: Markdown/notebook post rendering with executable code blocks
- **HTMX**: Tag filtering and partial page updates
- **Pixi**: Reproducible dependency management

## License

MIT
