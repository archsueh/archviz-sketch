"""archviz-sketch MCP server."""

from mcp.server.fastmcp import FastMCP
from .engine import get_prompt, list_styles

mcp = FastMCP("archviz-sketch")


@mcp.tool()
def archviz_sketch_generate(style: str, params: dict) -> str:
    """Generate a sketch illustration prompt.

    Args:
        style: Sketch style (process-draft, minimal-line, product-handdrawn, xiaohei)
        params: Parameters (subject, detail_level, angle, etc.)
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
