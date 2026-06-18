"""
archviz-sketch engine — prompt-driven sketch illustration pipeline.

Usage:
    from archviz_sketch.engine import get_prompt, list_styles

    prompt = get_prompt("process-draft", {"subject": "data pipeline architecture"})
"""

import json
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "templates" / "prompts"

STYLE_REGISTRY = {
    "process-draft": {
        "file": "process-draft.md",
        "description": "Process draft / working sketch — shows construction lines and iteration",
        "schema": {
            "subject": "str — what to draw",
            "detail_level": "str — 'minimal' | 'medium' | 'detailed' (default 'medium')",
        },
    },
    "minimal-line": {
        "file": "minimal-line.md",
        "description": "Minimal line drawing — clean single-weight lines, no shading",
        "schema": {
            "subject": "str — what to draw",
        },
    },
    "swiss-modernist": {
        "file": "swiss-modernist.md",
        "description": "Swiss Modernist / Vignelli grid style — objective layout, bold sans-serif lettering, hairline rules, single-accent identifier",
        "schema": {
            "subject": "str — what to draw",
        },
    },
    "product-handdrawn": {
        "file": "product-handdrawn.md",
        "description": "Product hand-drawn style — construction lines visible, imperfect feel",
        "schema": {
            "subject": "str — product or object to draw",
            "angle": "str — 'front' | 'side' | 'perspective' (default 'perspective')",
        },
    },
    "xiaohei": {
        "file": "xiaohei.md",
        "description": "Xiaohei style — pure white ground, black line art, 小黑 IP performing the core action, sparse handwritten annotations",
        "schema": {
            "subject": "str — what to draw",
        },
    },
    "watercolor": {
        "file": "watercolor.md",
        "description": "Watercolor hand illustration — ink contour + transparent blue-gray washes, for emotional narrative / scenes",
        "schema": {
            "subject": "str — what to draw",
        },
    },
    "architectural-marker": {
        "file": "architectural-marker.md",
        "description": "Architectural marker sketch — fineliner + loose gray marker, perspective, for spatial / building briefs",
        "schema": {
            "subject": "str — space or building to draw",
        },
    },
}


def list_styles() -> list[dict]:
    return [
        {"style": s, "description": info["description"], "schema": info["schema"]}
        for s, info in STYLE_REGISTRY.items()
    ]


def get_prompt(style: str, params: dict) -> str:
    """Load a prompt template and fill in parameters."""
    if style not in STYLE_REGISTRY:
        available = ", ".join(STYLE_REGISTRY.keys())
        raise ValueError(f"Unknown style '{style}'. Available: {available}")

    info = STYLE_REGISTRY[style]
    prompt_path = PROMPTS_DIR / info["file"]

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")

    prompt = prompt_path.read_text(encoding="utf-8")

    # Inject parameters. Templates use {{key}} canonical tokens (e.g. {{subject}}).
    # Single-brace {key} is also supported for convenience. Other single-brace
    # spans like {主题/核心隐喻} are intentional guidance for the agent to fill,
    # so we only substitute keys that were actually provided.
    for key, value in params.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", str(value))  # {{key}}
        prompt = prompt.replace(f"{{{key}}}", str(value))      # {key}

    return prompt
