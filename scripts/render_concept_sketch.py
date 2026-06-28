#!/usr/bin/env python3
"""
Enhanced hand-drawn chart renderer with Carl Liu style.
Reference: Industrial design concept sketch sheet
Features:
- Bold ink outlines + thin construction lines
- Selective color (only on key elements)
- Handwritten annotations with arrows
- Component breakdown diagrams
- Unfinished sketch feel
"""
import argparse
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Theme inspired by Carl Liu's style
CARL_LIU_THEME = {
    "bg": "#f5f0eb",  # Warm paper
    "ink": "#1a1a1a",  # Black ink
    "muted": "#8b7b6b",  # Muted brown
    "accent1": "#7b2d8e",  # Purple (primary)
    "accent2": "#2d8e7b",  # Teal
    "accent3": "#d4532a",  # Orange-red
    "annotation": "#4a6b8a",  # Blue-gray for annotations
}

SCALE = 2
DEFAULT_W = 1200
DEFAULT_H = 900
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
    """Draw hand-drawn line with wobble."""
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
    
    # Draw multiple slightly offset lines for ink effect
    for offset in [-0.5, 0, 0.5]:
        offset_points = [(x + offset, y + offset) for x, y in wobbled_points]
        draw.line(offset_points, fill=hex_rgba(color), width=max(1, c(width)), joint="curve")


def draw_arrow(draw, start, end, color, width=2):
    """Draw an arrow from start to end."""
    wobble_line(draw, [start, end], color, width)
    
    # Arrowhead
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 15
    spread = 0.5
    
    p1 = (end[0] - length * math.cos(angle - spread), 
          end[1] - length * math.sin(angle - spread))
    p2 = (end[0] - length * math.cos(angle + spread), 
          end[1] - length * math.sin(angle + spread))
    
    wobble_line(draw, [p1, end], color, width)
    wobble_line(draw, [p2, end], color, width)


def draw_annotation(draw, x, y, text, target_x, target_y, color=None):
    """Draw annotation with arrow pointing to target."""
    theme = CARL_LIU_THEME
    color = color or theme["annotation"]
    
    font = load_font(11, hand=True)
    
    # Draw text
    draw.text((c(x), c(y)), text, font=font, fill=hex_rgba(color))
    
    # Draw arrow from text to target
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    arrow_start = (x + text_width / SCALE + 5, y + text_height / SCALE / 2)
    draw_arrow(draw, arrow_start, (target_x, target_y), color, 1)


def draw_component_breakdown(draw, x, y, parts, theme):
    """Draw component breakdown diagram."""
    font_title = load_font(14, hand=True, bold=True)
    font_label = load_font(10, hand=True)
    
    # Title
    draw.text((c(x), c(y)), "COMPONENT BREAKDOWN", font=font_title, fill=hex_rgba(theme["ink"]))
    
    # Draw parts
    current_y = y + 25
    for i, part in enumerate(parts):
        name = part.get("name", f"Part {i+1}")
        color = [theme["accent1"], theme["accent2"], theme["accent3"]][i % 3]
        
        # Draw small box
        draw.rectangle(
            [c(x), c(current_y), c(x + 20), c(current_y + 15)],
            fill=hex_rgba(color),
            outline=hex_rgba(theme["ink"]),
        )
        
        # Draw label
        draw.text((c(x + 25), c(current_y)), name, font=font_label, fill=hex_rgba(theme["ink"]))
        
        current_y += 20


def render_frame(data, progress, width, height):
    """Render Carl Liu style concept sketch."""
    theme = CARL_LIU_THEME
    
    img = Image.new("RGBA", (width * SCALE, height * SCALE), hex_rgba(theme["bg"]))
    draw = ImageDraw.Draw(img)
    
    # Add paper texture
    rng = random.Random(42)
    for _ in range(5000):
        px = rng.randint(0, width * SCALE - 1)
        py = rng.randint(0, height * SCALE - 1)
        alpha = rng.randint(5, 20)
        draw.point((px, py), fill=hex_rgba(theme["muted"], alpha))
    
    # Title
    title = data.get("title", "CONCEPT DESIGN")
    font_title = load_font(28, bold=True, hand=True)
    draw.text((c(40), c(30)), title, font=font_title, fill=hex_rgba(theme["ink"]))
    
    # Subtitle
    subtitle = data.get("subtitle", "")
    if subtitle:
        font_sub = load_font(14, hand=True)
        draw.text((c(40), c(65)), subtitle, font=font_sub, fill=hex_rgba(theme["muted"]))
    
    # Main device (large, centered)
    device = data.get("device", {})
    reveal_progress = 0
    if device:
        # Draw device body
        dx = device.get("x", width / 2 - 100)
        dy = device.get("y", 120)
        dw = device.get("width", 200)
        dh = device.get("height", 300)
        
        # Animated reveal
        reveal_progress = min(progress * 1.5, 1.0)
        revealed_height = dh * reveal_progress
        
        # Draw device with selective color
        draw.rectangle(
            [c(dx), c(dy), c(dx + dw), c(dy + revealed_height)],
            fill=hex_rgba(theme["accent1"], 200),
            outline=hex_rgba(theme["ink"]),
            width=c(2),
        )
        
        # Draw construction lines (thin, muted)
        for i in range(5):
            y_line = dy + revealed_height * i / 4
            wobble_line(draw, [(dx - 20, y_line), (dx + dw + 20, y_line)], 
                       theme["muted"], 1, wobble=3)
        
        # Draw device details
        if reveal_progress > 0.5:
            # Screen
            draw.rectangle(
                [c(dx + 20), c(dy + 20), c(dx + dw - 20), c(dy + 80)],
                fill=hex_rgba(theme["accent2"], 150),
                outline=hex_rgba(theme["ink"]),
            )
            
            # Buttons
            for i in range(3):
                bx = dx + 30 + i * 50
                by = dy + revealed_height - 40
                draw.ellipse(
                    [c(bx), c(by), c(bx + 20), c(by + 20)],
                    fill=hex_rgba(theme["accent3"]),
                    outline=hex_rgba(theme["ink"]),
                )
    
    # Annotations
    annotations = data.get("annotations", [])
    if reveal_progress > 0.7:
        for anno in annotations:
            ax = anno.get("x", 0)
            ay = anno.get("y", 0)
            text = anno.get("text", "")
            tx = anno.get("target_x", width / 2)
            ty = anno.get("target_y", height / 2)
            
            draw_annotation(draw, ax, ay, text, tx, ty)
    
    # Component breakdown
    components = data.get("components", [])
    if components and reveal_progress > 0.8:
        draw_component_breakdown(draw, width - 250, 150, components, theme)
    
    # Signature
    font_sig = load_font(10, hand=True)
    draw.text((c(width - 150), c(height - 40)), "@archsueh", font=font_sig, fill=hex_rgba(theme["muted"]))
    
    return img


def render_carl_liu_style(data, outdir, basename, frames=DEFAULT_FRAMES, fps=DEFAULT_FPS):
    """Render Carl Liu style concept sketch animation."""
    width = data.get("width", DEFAULT_W)
    height = data.get("height", DEFAULT_H)
    
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    # Generate frames
    images = []
    for i in range(frames):
        progress = i / (frames - 1)
        frame = render_frame(data, progress, width, height)
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
    parser = argparse.ArgumentParser(description="Carl Liu style concept sketch renderer")
    parser.add_argument("--spec", required=True, help="JSON spec file")
    parser.add_argument("--outdir", default="./output", help="Output directory")
    parser.add_argument("--basename", default="concept", help="Output filename base")
    parser.add_argument("--frames", type=int, default=DEFAULT_FRAMES, help="Number of frames")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS, help="Frames per second")
    args = parser.parse_args()
    
    # Load spec
    with open(args.spec, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Render
    gif_path, png_path = render_carl_liu_style(
        data, args.outdir, args.basename, args.frames, args.fps
    )
    
    print(f"\nDone! Generated:")
    print(f"  - {gif_path}")
    print(f"  - {png_path}")


if __name__ == "__main__":
    main()
