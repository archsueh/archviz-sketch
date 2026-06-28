#!/usr/bin/env python3
"""
Hand-drawn style bar chart renderer.
Cross-optimization: archviz-sketch + archviz-diagram
Styles: xiaohei (black line art), minimal-line (thin lines + color accents)
"""
import argparse
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Theme for hand-drawn style
THEMES = {
    "xiaohei": {
        "bg": "#ffffff",
        "line": "#1a1a1a",
        "accent": "#e74c3c",
        "secondary": "#3498db",
        "muted": "#95a5a6",
        "annotation": "#e67e22",
    },
    "minimal-line": {
        "bg": "#fafafa",
        "line": "#2c3e50",
        "accent": "#e74c3c",
        "secondary": "#3498db",
        "muted": "#95a5a6",
        "annotation": "#2ecc71",
    },
    "process-draft": {
        "bg": "#f5f0eb",
        "line": "#1a1a1a",
        "accent": "#002fa7",
        "secondary": "#c96442",
        "muted": "#a8a29e",
        "annotation": "#c96442",
    },
}

SCALE = 2
DEFAULT_W = 800
DEFAULT_H = 500
DEFAULT_FPS = 15
DEFAULT_FRAMES = 30


def hex_rgba(value, alpha=255):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def c(v):
    return int(round(v * SCALE))


def load_font(size, bold=False, hand=False):
    candidates = []
    if hand:
        candidates = [
            "/System/Library/Fonts/Supplemental/Chalkduster.ttf",
            "/System/Library/Fonts/MarkerFelt.ttc",
            "/System/Library/Fonts/Noteworthy.ttc",
        ]
    candidates.extend([
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ])
    for path in candidates:
        try:
            return ImageFont.truetype(path, c(size))
        except OSError:
            continue
    return ImageFont.load_default()


def wobble_line(draw, points, color, width=2, wobble=2):
    """Draw a hand-drawn style line with slight wobble."""
    if len(points) < 2:
        return
    
    rng = random.Random(hash(str(points)))
    wobbled_points = []
    for i, (x, y) in enumerate(points):
        if i == 0 or i == len(points) - 1:
            wobbled_points.append((c(x), c(y)))
        else:
            dx = rng.uniform(-wobble, wobble)
            dy = rng.uniform(-wobble, wobble)
            wobbled_points.append((c(x + dx), c(y + dy)))
    
    # Draw multiple slightly offset lines for hand-drawn effect
    for offset in [-0.5, 0, 0.5]:
        offset_points = [(x + offset, y + offset) for x, y in wobbled_points]
        draw.line(offset_points, fill=hex_rgba(color), width=max(1, c(width)), joint="curve")


def wobble_rect(draw, x, y, w, h, color, fill=None, width=2, wobble=3):
    """Draw a hand-drawn style rectangle."""
    # Skip if height is too small
    if h < 2:
        return
    
    # Draw with slight wobble on each side
    points = [
        (x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)
    ]
    wobble_line(draw, points, color, width, wobble)
    
    if fill:
        # Fill with slightly transparent color
        draw.rectangle(
            [c(x + 2), c(y + 2), c(x + w - 2), c(y + h - 2)],
            fill=hex_rgba(fill, 200)
        )


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def render_frame(data, progress, width, height, style="xiaohei"):
    """Render a single frame of hand-drawn bar chart."""
    theme = THEMES.get(style, THEMES["xiaohei"])
    
    img = Image.new("RGBA", (width * SCALE, height * SCALE), hex_rgba(theme["bg"]))
    draw = ImageDraw.Draw(img)
    
    # Add paper texture for process-draft style
    if style == "process-draft":
        rng = random.Random(42)
        for _ in range(1000):
            px = rng.randint(0, width * SCALE - 1)
            py = rng.randint(0, height * SCALE - 1)
            alpha = rng.randint(10, 30)
            draw.point((px, py), fill=hex_rgba(theme["muted"], alpha))
    
    # Layout
    margin_left = 80
    margin_right = 40
    margin_top = 60
    margin_bottom = 80
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    
    # Title (hand-drawn style)
    title = data.get("title", "Chart")
    font_title = load_font(24, bold=True, hand=True)
    draw.text(
        (c(margin_left), c(20)),
        title,
        font=font_title,
        fill=hex_rgba(theme["line"]),
    )
    
    # Subtitle
    subtitle = data.get("subtitle", "")
    if subtitle:
        font_sub = load_font(14, hand=True)
        draw.text(
            (c(margin_left), c(48)),
            subtitle,
            font=font_sub,
            fill=hex_rgba(theme["muted"]),
        )
    
    # Data
    categories = data.get("categories", [])
    values = data.get("values", [])
    labels = data.get("labels", [])
    
    if not categories or not values:
        return img
    
    # Calculate bar width
    n_bars = len(categories)
    bar_width = min(60, chart_width / n_bars * 0.7)
    gap = (chart_width - bar_width * n_bars) / (n_bars + 1)
    
    # Max value for scaling
    max_val = max(values) if values else 1
    
    # Draw axes (hand-drawn style)
    wobble_line(draw, [(margin_left, margin_top), (margin_left, margin_top + chart_height)], theme["line"], 2)
    wobble_line(draw, [(margin_left, margin_top + chart_height), (width - margin_right, margin_top + chart_height)], theme["line"], 2)
    
    # Draw bars with animation
    font_label = load_font(12, hand=True)
    font_value = load_font(11, hand=True)
    
    for i, (cat, val) in enumerate(zip(categories, values)):
        # Animated height
        animated_progress = ease_out_cubic(min(progress * 1.2 - i * 0.05, 1.0))
        animated_progress = max(0, animated_progress)
        
        bar_height = (val / max_val) * chart_height * animated_progress
        x = margin_left + gap + i * (bar_width + gap)
        y = margin_top + chart_height - bar_height
        
        # Bar color (cycle through accent colors)
        colors = [theme["accent"], theme["secondary"], theme["annotation"]]
        color = colors[i % len(colors)]
        
        # Draw hand-drawn bar
        wobble_rect(draw, x, y, bar_width, bar_height, theme["line"], fill=color, wobble=4)
        
        # Category label
        label = labels[i] if i < len(labels) else cat
        bbox = draw.textbbox((0, 0), label, font=font_label)
        label_width = bbox[2] - bbox[0]
        draw.text(
            (c(x + bar_width / 2 - label_width / 2 / SCALE), c(margin_top + chart_height + 10)),
            label,
            font=font_label,
            fill=hex_rgba(theme["line"]),
        )
        
        # Value label
        if animated_progress > 0.8:
            value_text = f"{val:.1f}"
            bbox = draw.textbbox((0, 0), value_text, font=font_value)
            value_width = bbox[2] - bbox[0]
            draw.text(
                (c(x + bar_width / 2 - value_width / 2 / SCALE), c(y - 20)),
                value_text,
                font=font_value,
                fill=hex_rgba(theme["accent"]),
            )
    
    # Y-axis labels
    for i in range(5):
        val = max_val * i / 4
        y = margin_top + chart_height - (val / max_val) * chart_height
        
        # Tick mark
        wobble_line(draw, [(margin_left - 5, y), (margin_left, y)], theme["line"], 1)
        
        # Label
        label = f"{val:.0f}"
        bbox = draw.textbbox((0, 0), label, font=font_value)
        label_width = bbox[2] - bbox[0]
        draw.text(
            (c(margin_left - 10 - label_width / SCALE), c(y - 6)),
            label,
            font=font_value,
            fill=hex_rgba(theme["muted"]),
        )
    
    # Add hand-drawn annotations (for xiaohei style)
    if style == "xiaohei":
        font_anno = load_font(10, hand=True)
        # Add a small annotation
        anno_x = width - margin_right - 100
        anno_y = margin_top + 20
        draw.text(
            (c(anno_x), c(anno_y)),
            "手绘风格",
            font=font_anno,
            fill=hex_rgba(theme["annotation"]),
        )
    
    return img


def render_hand_drawn_chart(data, outdir, basename, style="xiaohei", frames=DEFAULT_FRAMES, fps=DEFAULT_FPS):
    """Render hand-drawn bar chart as GIF."""
    width = data.get("width", DEFAULT_W)
    height = data.get("height", DEFAULT_H)
    
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    # Generate frames
    images = []
    for i in range(frames):
        progress = i / (frames - 1)
        frame = render_frame(data, progress, width, height, style)
        images.append(frame)
    
    # Save GIF
    gif_path = outdir / f"{basename}.gif"
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=int(1000 / fps),
        loop=0,
    )
    print(f"GIF saved: {gif_path}")
    
    # Save static PNG
    png_path = outdir / f"{basename}.png"
    images[-1].save(png_path)
    print(f"PNG saved: {png_path}")
    
    return gif_path, png_path


def main():
    parser = argparse.ArgumentParser(description="Hand-drawn style bar chart renderer")
    parser.add_argument("--spec", required=True, help="JSON spec file")
    parser.add_argument("--outdir", default="./output", help="Output directory")
    parser.add_argument("--basename", default="chart", help="Output filename base")
    parser.add_argument("--style", default="xiaohei", choices=["xiaohei", "minimal-line", "process-draft"], help="Drawing style")
    parser.add_argument("--frames", type=int, default=DEFAULT_FRAMES, help="Number of frames")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Frames per second")
    args = parser.parse_args()
    
    # Load spec
    with open(args.spec, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Render
    gif_path, png_path = render_hand_drawn_chart(
        data, args.outdir, args.basename, args.style, args.frames, args.fps
    )
    
    print(f"\nDone! Generated:")
    print(f"  - {gif_path}")
    print(f"  - {png_path}")


if __name__ == "__main__":
    main()
