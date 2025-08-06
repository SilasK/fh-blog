<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# FastHTML Blog Project Instructions

This is a FastHTML blog application that uses markdown files for content and supports live Python code execution in blog posts.

## Project Structure

- `app.py` - Main FastHTML application
- `posts/` - Directory containing markdown blog posts with YAML frontmatter
- `pyproject.toml` - Pixi project configuration

## Key Technologies

- **FastHTML**: Modern Python web framework
- **Pixi**: Package manager for reproducible environments

## Development Guidelines

When working on this project:

1. **Blog Posts**: All posts should include YAML frontmatter with `title`, `date`, `author`, `excerpt`, and `slug` fields
2. **Code Execution**: Use `python:run` code blocks for executable code in posts
3. **Styling**: Keep styling minimal and clean, focusing on readability
4. **Routes**: Use FastHTML's routing system with `@rt` decorator
5. **Package Management**: Use pixi commands (not pip) for dependency management

## Code Style

- Follow Python best practices
- Use FastHTML's component system for reusable UI elements
- Keep the app.py file organized with clear route definitions
- Use meaningful variable names and add comments for complex logic

## Testing Posts

- Test code blocks before publishing posts
- Ensure YAML frontmatter is valid
- Check that slug values are unique and URL-friendly
