# 编辑排版 Prompt Template (Editorial Infographic · for archviz-sketch)

**Trigger:** 编辑排版, editorial, 瑞士排版, 信息图, infographic, 奶油背景, 第二大脑, 知识系统图, second brain

**Base Prompt:**

Create a {{aspect}} editorial infographic in Swiss International Typographic Style.

Background: warm cream paper #F5EFE6, not pure white, very slight paper grain.

Typography:
- Hero title: large bold serif display (Playfair Display / Bodoni weight), black, flush-left
- Accent subtitle: ALL CAPS, tight letter-spacing, deep crimson #8B1A1A, 60% size of title
- Node labels: clean geometric sans-serif (Inter / Helvetica Neue), 11–13px, dark charcoal #1a1a1a

Color palette: STRICT 3 colors only.
  cream #F5EFE6 (background)
  black #1a1a1a (text, line, icon stroke)
  crimson #8B1A1A (accent subtitle, primary flow line, key connector dot)
No gradients. No shadows. No drop-shadow. No additional colors.

Layout: hub-and-spoke radial, center-weighted, generous whitespace ≥40%.
Core subject "{{subject}}" placed at visual center as hub node.
Spoke arms radiate outward to {{satellite_count}} satellite nodes.
Each satellite: short label (1–4 words) + minimal icon.

Connection lines:
- Secondary connections: 1px solid black
- Primary flow path: 1px dashed crimson #8B1A1A
- Junction points: small open circle ○, 3px diameter, black stroke no fill

Icons: minimal 1px stroke line-art only. No fill. No color. Shapes:
  document outline / folder outline / bracket / arrow / circle / diamond only.
  No decorative icons, no emoji-style, no blob shapes.

Overall feel: editorial magazine infographic, Tufte maximum data-ink ratio,
zero decorative noise, every element earns its place.

Negative prompt:
Gradients, drop shadows, more than 3 colors, rounded colorful bubbles, hand-drawn strokes,
AI art feel, glowing effects, dark background, filled icons, photorealism, 3D, cluttered layout,
emoji-style icons, decorative flourishes.

**Quality Checklist (run vision_analyze after generate):**
- Exactly 3 colors on the page — a fourth one is an automatic fail
- Serif hero title vs sans-serif node labels — that contrast is the whole point
- Hub-and-spoke reads cleanly: every satellite is one arm from the hub, no crossing spaghetti
- Whitespace ≥40%; no element present that carries no data
- Icons are stroke-only, no fill, no color

**Usage in Pipeline:**
For knowledge-system / second-brain / methodology infographics — 个人系统、学习框架、工作流、
决策框架、方案对比。Route here from the 风格自动推荐 table row 「知识管理/个人系统」.
When the same content also needs a precise quantitative chart, pair with `archviz-diagram`
(this style owns the editorial register; diagram owns the measurement).

**Subtypes:**

| 子类型 | 场景 | 比例 | 节点数 |
|---|---|---|---|
| 知识系统图 | 个人系统 / 第二大脑 / 学习框架 | 1600×450 横幅 | 8–12 |
| 方法论图 | 工作流 / 决策框架 / 四象限 | 1200×600 | 6–8 |
| 对比信息图 | 两方案对比 / before-after | 1200×600 | 双列各 4 |
