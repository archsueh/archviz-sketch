# 建筑马克笔 Prompt Template (for archviz-sketch)

**Trigger:** 建筑马克笔, 建筑手绘, 空间设计, 透视

**Base Prompt:**

Create a 2K architectural marker sketch for "{{subject}}".

Style: Black fineliner linework + pencil construction + loose gray marker shadows on white paper.
Expressive perspective with scale figures for human reference. Large breathing white space.

Composition: {空间视角, e.g. 街景透视 / 室内一角 / 鸟瞰}. Annotations: {材料/尺度标注词}.

Key requirements:
- Confident fineliner outline, visible pencil construction/perspective guides
- Gray marker used loosely for shadow and depth only (not full fills)
- One or two scale figures to convey human scale
- Generous white space (≥40%); never fill the whole frame
- Slight hand imperfection — this is a design sketch, not a CAD render

Negative prompt:
Photorealistic arch-viz, CAD precision, glossy 3D render, heavy color fills, cluttered composition, no construction lines.

**Quality Checklist (run vision_analyze after generate):**
- Perspective reads correctly with construction hints visible
- Marker shadows loose, not solid fills
- Scale figure present
- High 留白, restrained gray + ink only

**Usage in Pipeline:**
For spatial / building / interior briefs. Route here from archviz-3d when the deliverable is a hand sketch rather than an interactive 3D model.

**400-free reference:** Architectural marker / urban sketching references for perspective looseness.
