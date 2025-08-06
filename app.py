from fasthtml.common import *
from monsterui.all import *
from fh_posts.all import *
import os
import yaml


# Load configuration
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


config = load_config()

app, rt = fast_app(
    hdrs=(
        Theme[config["theme"]["primary_color"]].headers(mode="light"),
        HighlightJS(
            langs=config["theme"]["supported_languages"],
            light=config["theme"]["code_highlight_theme"],
        ),
    ),
    live=True,
)


def twitter_headers(post: Post = None):
    """Generate meta tags for Twitter Cards and Open Graph (works for LinkedIn, Facebook, etc.)"""
    if post:
        return (
            # Twitter Card tags
            Meta(name="twitter:card", content="summary"),
            Meta(name="twitter:title", content=post.title),
            Meta(
                name="twitter:description",
                content=post.summary if post.summary else config["blog"]["description"],
            ),
            Meta(name="twitter:image", content=config["seo"]["twitter_card_image"]),
            # Open Graph tags (for LinkedIn, Facebook, etc.)
            Meta(property="og:type", content="article"),
            Meta(property="og:title", content=post.title),
            Meta(
                property="og:description",
                content=post.summary if post.summary else config["blog"]["description"],
            ),
            Meta(property="og:image", content=config["seo"]["twitter_card_image"]),
            Meta(
                property="og:url", content=f"{config['blog']['url']}/post/{post.slug}"
            ),
            Meta(property="og:site_name", content=config["blog"]["title"]),
        )
    else:
        return (
            # Twitter Card tags
            Meta(name="twitter:card", content="summary"),
            Meta(name="twitter:title", content=config["blog"]["title"]),
            Meta(name="twitter:description", content=config["blog"]["subtitle"]),
            Meta(name="twitter:image", content=config["seo"]["twitter_card_image"]),
            # Open Graph tags (for LinkedIn, Facebook, etc.)
            Meta(property="og:type", content="website"),
            Meta(property="og:title", content=config["blog"]["title"]),
            Meta(property="og:description", content=config["blog"]["subtitle"]),
            Meta(property="og:image", content=config["seo"]["twitter_card_image"]),
            Meta(property="og:url", content=config["blog"]["url"]),
            Meta(property="og:site_name", content=config["blog"]["title"]),
        )


def SocialLink(icon, url, text=""):
    """Creates a social media link with icon"""
    return A(
        DivLAligned(UkIcon(icon), P(text, cls=TextPresets.md_weight_sm)),
        href=url,
        target="_blank",
        rel="noopener noreferrer",
        cls="hover:text-gray-500 duration-200",
    )


def get_social_links():
    """Generate social links from config"""
    links = []
    social_config = config["social"]

    for platform, settings in social_config.items():
        if settings.get("display", False):
            icon = platform.lower()

            links.append(SocialLink(icon, settings["url"]))

    return links


def BlogPostCard(post):
    """Creates a card for a blog post preview"""
    return A(
        Card(
            DivVStacked(
                H3(post.title, cls=TextPresets.bold_lg),
                P(post.date, cls=TextPresets.muted_sm),
                P(post.summary, cls=TextPresets.muted_sm),
                # Updated tags section with smaller, more compact styling
                DivLAligned(
                    *[
                        P(
                            tag.replace("-", " "),
                            cls=TextT.xs
                            + TextT.muted
                            + " bg-gray-50 px-1.5 rounded mr-1",
                        )
                        for tag in post.tags
                    ],
                    cls="flex-wrap mt-2",
                ),
                cls="h-full",  # Make the inner content container full height; makes all the cards the same height
            ),
            cls="hover:shadow-lg transition-shadow duration-200 h-full",  # Make card full height
        ),
        href=f"/post/{post.slug}",
    )


def TagButton(tag, is_selected=False, cls=""):
    """Creates a clickable tag button with selected state using HTMX"""
    base_cls = (
        "px-3 py-1 rounded-full text-sm transition-colors duration-200 cursor-pointer"
    )
    selected_cls = (
        "bg-gray-800 text-white"
        if is_selected
        else "bg-gray-200 hover:bg-gray-300 text-gray-700"
    )

    if is_selected:
        # If selected, clicking should clear the filter
        return Button(
            tag.replace("-", " "),
            hx_get="/posts-container",
            hx_target="#posts-container",
            hx_swap="outerHTML",
            cls=f"{base_cls} {selected_cls} {cls}",
        )
    else:
        # If not selected, clicking should filter by this tag
        return Button(
            tag.replace("-", " "),
            hx_get=f"/posts-container?tag={tag}",
            hx_target="#posts-container",
            hx_swap="outerHTML",
            cls=f"{base_cls} {selected_cls} {cls}",
        )


def get_posts_container(tag: str = None):
    """Helper function to generate the posts container content"""
    # Load posts
    posts = load_posts("posts")

    # Filter posts if tag is provided
    filtered_posts = [
        post
        for post in posts
        if (not tag or tag in post.tags) and not post.metadata.get("draft", False)
    ]

    # Get tag frequencies and sort by most common, then alphabetically for ties
    tag_freq = {}
    for post in posts:
        if not post.metadata.get("draft", False):
            for t in post.tags:
                tag_freq[t] = tag_freq.get(t, 0) + 1

    # Get top 5 tags sorted by frequency (and alphabetically for ties)
    top_tags = sorted(tag_freq.items(), key=lambda x: (-x[1], x[0]))[:5]
    top_tags = [t[0] for t in top_tags]

    return DivVStacked(
        H3("Latest Posts"),
        # Top 5 tags filter
        DivLAligned(
            *[TagButton(t, is_selected=(t == tag), cls="mr-2 mb-2") for t in top_tags],
            cls="flex-wrap",
        ),
        Grid(
            *[
                BlogPostCard(post)
                for post in filtered_posts[: config["settings"]["posts_per_page"]]
            ],
            cols_sm=1,
            cols_md=1,
            cols_lg=1,
            cols_xl=1,
            cols_2xl=1,
            gap=6,
        ),
        id="posts-container",
    )


@rt("/posts-container")
def get_posts_container_route(tag: str = None):
    """Route that returns just the posts container for HTMX updates"""
    return get_posts_container(tag)


@rt("/")
def get(tag: str = None):
    # Load posts on each request
    posts = load_posts("posts")

    # Filter posts if tag is provided
    filtered_posts = [
        post
        for post in posts
        if (not tag or tag in post.tags) and not post.metadata.get("draft", False)
    ]

    # Get tag frequencies and sort by most common, then alphabetically for ties
    tag_freq = {}
    for post in posts:
        if not post.metadata.get("draft", False):
            for t in post.tags:
                tag_freq[t] = tag_freq.get(t, 0) + 1

    # Get top 5 tags sorted by frequency (and alphabetically for ties)
    top_tags = sorted(tag_freq.items(), key=lambda x: (-x[1], x[0]))[:5]
    top_tags = [t[0] for t in top_tags]

    return (
        *twitter_headers(),
        Title(config["blog"]["title"]),
        Container(
            # Header section
            DivVStacked(
                A(H1(config["blog"]["title"], cls="mt-8"), href="/"),
                P(
                    config["blog"]["subtitle"],
                    cls=TextPresets.muted_lg,
                ),
                # Social links from config
                DivLAligned(
                    *get_social_links(),
                    cls="space-x-6 mt-4",
                ),
                Divider(cls="my-8"),
            ),
            # Blog posts section - use the helper function
            get_posts_container(tag),
            cls="max-w-4xl mx-auto px-4 py-8",
        ),
    )


@rt("/post/{post_slug}")
def get(post_slug: str):
    # Load posts on each request
    posts = load_posts("posts")

    # Find the post or return 404
    post = next((p for p in posts if p.slug == post_slug), None)
    if not post:
        return Title("404 - Aw, man!"), Container(
            H1("404 - Aw, man!", cls="text-4xl font-bold mt-8"),
            P(
                "The post you're looking for doesn't exist but I bet it would have been a good one.",
                cls=TextPresets.muted_lg,
            ),
            A("← Back to Home", href="/", cls="text-black hover:text-gray-600 mt-4"),
        )

    # Process the content and get HTML
    rendered_content = post.render(open_links_new_window=True)

    return (
        *twitter_headers(post),
        Title(f"{post.title} - {config['blog']['title']}"),
        Container(
            DivVStacked(
                # Back link
                A("← Back to Home", href="/", cls="hover:text-gray-600 mb-8"),
                # Post header
                H1(post.title),
                P(post.date, cls=TextPresets.muted_lg + " mt-2"),
                Divider(cls="my-8"),
                cls="w-full",  # Ensure inner content respects container width
            ),
            # Post content with executed code blocks
            Article(rendered_content),
            cls="max-w-4xl mx-auto px-4 py-8",  # Added w-full
        ),
    )


if __name__ == "__main__":
    serve(port=8001, reload=True)
