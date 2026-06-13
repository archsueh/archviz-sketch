"""archviz-sketch MCP server."""

from mcp.server.fastmcp import FastMCP
from .engine import get_prompt, list_styles

mcp = FastMCP("archviz-sketch")


@mcp.tool()
def archviz_sketch_generate(style: str, params: dict) -> str:
    """Build an image-generation PROMPT for a sketch illustration (returns text, NOT an image).

    This tool does prompt engineering only. To produce the actual image, pass the
    returned prompt to your configured image-generation tool (e.g. an `image_generate`
    tool wired to xAI/Grok, FAL, or OpenAI). API keys live in that tool's config,
    never here.

    Args:
        style: One of process-draft, minimal-line, product-handdrawn, xiaohei,
            watercolor, architectural-marker.
        params: Fields injected into the template. `subject` (str) is required;
            other fields named in the template guidance are filled by the agent.
    """
    try:
        return get_prompt(style, params)
    except (ValueError, FileNotFoundError) as e:
        return f"Error: {e}"


@mcp.tool()
def archviz_sketch_list_styles() -> str:
    """List available sketch styles with schemas."""
    import json
    styles = list_styles()
    result = []
    for s in styles:
        result.append(f"### {s['style']}\n{s['description']}\n\n**Schema:**\n```json\n{json.dumps(s['schema'], indent=2)}\n```\n")
    return "\n".join(result)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
