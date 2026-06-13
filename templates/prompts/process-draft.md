# Process Draft Prompt Template (核心风格 for archviz-sketch)

**Trigger:** 过程稿, 作图痕迹, 草稿感, 推演, 迭代

**Base Prompt (use as template, fill {vars}):**

Create a high-resolution image on off-white notebook paper background.

Draw "{主题/核心概念}" in a loose hand-drawn process-draft style using blue ballpoint pen or black marker.

Key requirements for process-gao feel:
- Visible construction lines, perspective guides, grid boxes, measurement ticks
- Side trials, crossed-out attempts, variant explorations in margins
- Handwritten annotations in Chinese/English: {标注列表, e.g. 结构/留白/重心}
- Imperfect: inconsistent line weight, uneven spacing, accidental overdraw, scratchy pressure, eraser ghosts
- Subject-related doodles around edges
- Composition: main idea 40-60%, plenty of white space (≥35% empty), natural paper texture

Avoid: clean vector art, perfect alignment, glossy rendering, photorealism, digital gradients, polished final look, no construction lines.

**Sub-variants:**
- 圆珠笔草稿: emphasize pressure variation and ink bleed
- 字体探索: focus on structure analysis, 笔画对比, 借形
- 设计推演: multiple parallel schemes with "划掉" marks and arrows between iterations

**Quality Checklist (run vision_analyze after generate):**
- Construction lines clearly visible
- Imperfect/hand-made energy present
- Annotations readable but wobbly
- No clean CAD look

**Usage in Pipeline:**
1. Content analysis identifies "推演" or "迭代" anchor.
2. Fill {主题} and {标注}.
3. Generate → inspect → refine prompt with more "visible guides" if needed.
4. Deliver with strategy note: "This is the thinking process, not the final polished version."

**Related 400-free ref:** Open Doodles, Lukasz Adam hand-drawn for style reference.
