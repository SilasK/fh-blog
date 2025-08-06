# Silas Kieser's Blog

This blog is built using [FastHTML](https://fastht.ml) and [MonsterUI](https://monsterui.answer.ai), showcasing the power of Python for full-stack web development.

## Features

- **Dynamic Content**: Blog posts support live Python code execution using the `fh-posts` library
- **Modern UI**: Beautiful, responsive design powered by MonsterUI
- **Tag Filtering**: Posts can be filtered by tags
- **Fast Development**: Built entirely in Python with FastHTML
- **Configurable**: Easy configuration through `config.yaml`

## Technology Stack

- **FastHTML**: Modern Python web framework for full-stack development
- **MonsterUI**: Beautiful UI components and styling
- **fh-posts**: Library for dynamic blog posts with executable code blocks
- **Pixi**: Package manager for reproducible environments

## Configuration

The blog is configured through `config.yaml`. You can customize:

- **Blog settings**: Title, subtitle, description, URL
- **Author information**: Name, email, bio
- **Social media links**: GitHub, Twitter, Bluesky, LinkedIn, Mastodon
- **SEO settings**: Meta tags, Twitter card images
- **Theme settings**: Colors, code highlighting, supported languages
- **Display settings**: Posts per page, features to enable/disable

### Example Configuration

```yaml
blog:
  title: "Your Blog Title"
  subtitle: "Your blog subtitle"
  
author:
  name: "Your Name"
  email: "your@email.com"
  
social:
  github:
    username: "yourusername"
    url: "https://github.com/yourusername"
    display: true
  bluesky:
    username: "yourusername.bsky.social"
    url: "https://bsky.app/profile/yourusername.bsky.social" 
    display: true
```

## Development

This project uses Pixi for dependency management. To get started:

```bash
# Install dependencies
pixi install

# Run the development server
pixi run dev
```

The blog will be available at http://localhost:8001

## Blog Posts

Posts are written in Markdown with YAML frontmatter and support:
- Live Python code execution with `python:run` code blocks
- Tag categorization
- Automatic slug generation
- Rich formatting with MonsterUI components

## Author

**Silas Kieser** - Sharing what I'm learning, teaching, and exploring in technology.

- GitHub: [@silas](https://github.com/silas)
- Twitter: [@silaskieser](https://twitter.com/silaskieser)
