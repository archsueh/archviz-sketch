# 水彩手绘 Prompt Template (for archviz-sketch)

**Trigger:** 水彩, watercolor, 情感叙事, 场景

**Base Prompt:**

Create a 2K transparent watercolor hand illustration of "{{subject}}".

Visual language: Delicate ink contour lines, transparent blue-gray washes, pale beige tones.
Watery edges, pigment blooms, unfinished white margins, soft bleed where washes meet.

Composition: {主体 + 场景氛围}. Mood: {情绪关键词, e.g. 安静 / 怀旧 / 温柔}.

Key requirements:
- Loose ink outline first, then transparent washes on top (never fully opaque)
- Visible water edges and granulation; let some areas stay raw paper white
- Restrained palette: blue-gray dominant + one warm accent max
- Hand-made imperfection: uneven wash density, slight bleed beyond lines

Negative prompt:
Photorealistic, glossy CGI, anime style, flat vector, heavy saturated fills, digital gradients, perfect clean edges.

**Quality Checklist (run vision_analyze after generate):**
- Ink contour visible under the washes
- Washes transparent, paper showing through
- Edges feel watery, not crisp
- Palette restrained (blue-gray + ≤1 accent)

**Usage in Pipeline:**
For emotional narrative, scene-setting, personal essays. Pair with minimal-line for cover + interior contrast.

**400-free reference:** Loose watercolor / ink-wash references for edge and bloom behavior.
