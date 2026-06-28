---
name: archviz-sketch
description: |
  文章配图全流程：内容分析 → 配图策略 → Prompt工程 → 出图 → 视觉质检 → 交付。
  8种风格，核心差异化：过程稿/作图痕迹（线稿可见、构造线外露、不完美的手作感）。
  需要 image_generate 工具（API由用户自行配置）。
  触发词：配图、插图、sketch、手绘、过程稿、作图痕迹、小黑风格、线条艺术
tags: [illustration, sketch, image-generation, pipeline, creative, process-draft]
version: 0.0.3
author: archsueh
license: MIT
---

# Sketch Pipeline

文章配图全流程管线。**核心差异化：过程稿/作图痕迹**——保留构造线、草稿感、不完美的手作能量。

---

## 架构

```
[1] 内容分析 ← 读文章，找认知锚点
     ↓
[2] 配图策略 ← 决定在哪插、插什么、用什么风格
     ↓
[3] Prompt工程 ← 每张图一个精确prompt（核心能力）
     ↓
[4] 出图 ← 调 image_generate（API由用户配置）
     ↓
[5] 视觉质检 ← vision_analyze 看图检查
     ↓
[6] 重试/交付 ← 不合格改prompt重来
```

---

## [1] 内容分析

读文章（文件路径或粘贴文本），提取：

| 提取项 | 说明 |
|---|---|
| 核心论点 | 2-5个，每个一句话 |
| 认知锚点 | 哪些段落需要图（核心判断/断点/闭环/分流/对比/隐喻） |
| 内容类型 | 技术/教程/方法论/叙事/学术 |
| 视觉关键词 | 可转化为画面的词 |

**不要平均配图。** 只在认知锚点处插图。

---

## [2] 配图策略

```yaml
article: "文章标题"
content_type: "设计日志"
total_images: 3
images:
  - id: 01
    position: "第2段后"
    purpose: "解释三层架构"
    style: "小黑怪诞"
    core_idea: "小黑在三层之间循环"
    labels: ["物质层", "思维层", "情感层"]
  - id: 02
    position: "第5段后"
    style: "过程稿"
    purpose: "展示设计迭代过程"
```

### 风格自动推荐

| 文章类型 | 推荐风格 |
|---|---|
| 产品设计 | 产品手绘 + 小黑 |
| 学术论文 | 极简线条 |
| 设计日志 | **过程稿** + 小黑 |
| 教学内容 | 小黑 |
| 个人叙事 | 水彩 + 小黑 |
| 技术博客 | 小黑 + 极简线条 |
| 知识管理/个人系统 | **编辑排版** |

用户可覆盖。

---

## [3] Prompt工程

8种风格，每种独立prompt模板。

### 风格总览

| 风格 | 适用 | 视觉特征 |
|---|---|---|
| **过程稿** ★ | 设计迭代、字体探索、作图痕迹 | 圆珠笔、笔记本纸、构造线外露、不完美 |
| **小黑怪诞** | 概念解释、流程、隐喻 | 纯白底、黑色线稿、小黑IP、中文批注 |
| **极简线条** | 封面、海报、概念视觉 | 细线、色彩点缀、大量留白 |
| **产品手绘** | 产品设计、结构展示 | 铅笔+马克笔、爆炸图、剖切图 |
| **水彩手绘** | 情感叙事、场景 | 透明水洗、墨线轮廓、蓝灰色调 |
| **建筑马克笔** | 空间设计、建筑展示 | 针管笔+马克笔、透视、留白 |
| **瑞士网格** | 扁平海报、客观布局、路网标识 | 严格网格、粗黑无衬线大字、细定位线、单色标识 |
| **编辑排版** | 知识信息图、个人系统展示 | 奶油底、衬线大标题、深红+黑严格三色、辐射布局 |

★ = 核心差异化风格

---

### 3a. 过程稿（Process Draft）★

**本质：保留作图痕迹的图。** 不是成品，是"正在画"的状态。

```text
Create a {分辨率} image on off-white notebook paper.

Draw "{短语/主题}" large and readable, loosely {风格} style.
{工具：blue ballpoint pen / black marker / pencil}

Key: show the making process, not the final result.
- Visible construction lines, perspective guides, grid boxes
- Measurement ticks, arrows, alignment marks
- Side trials, crossed-out attempts, variant explorations
- Handwritten annotations in margins: {标注词列表}
- Subject-related doodles: {相关涂鸦}

Keep it imperfect:
- Inconsistent line weight
- Uneven spacing
- Accidental overdraw
- Scratchy pressure marks
- Eraser ghosts

Negative prompt:
Exclude clean vector, glossy rendering, photorealism, perfect alignment,
poster grids, digital gradients, polished final look.
```

**过程稿子类型：**

| 子类型 | 触发词 | 工具 | 特征 |
|---|---|---|---|
| 圆珠笔草稿 | "过程稿""手稿""圆珠笔" | 蓝色圆珠笔 | 压力不均、墨迹 |
| 字体探索 | "爨体""字体设计""字形变体" | 圆珠笔/马克笔 | 结构标注、笔画分析 |
| 产品草图 | "产品手绘""造型基础" | 铅笔+针管笔 | 透视线、椭圆、尺寸标注 |
| 设计推演 | "推演""迭代""方案对比" | 混合工具 | 多方案并列、划掉的方案 |

**标注词系统：**

```
设计类：同构 / 异构 / 开合 / 重心 / 疏密 / 中宫 / 外放 / 收紧
字体类：借形 / 共用笔画 / 笔画替换 / 结构对比 / 字形变体 / 负形
通用类：留白 / 字距 / 行距 / 粗细对比 / 视觉平衡 / 节奏 / 轴线
英文：spacing / structure / balance / rhythm / axis / weight contrast
```

---

### 3b. 小黑怪诞（Xiaohei）

```text
Generate one standalone 16:9 horizontal Chinese article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines.
Lots of empty white space. Sparse red/orange/blue handwritten Chinese annotations.
Clean absurd product-sketch feeling. No gradients, no shadows, no paper texture.

Recurring IP character:
小黑, a small solid-black absurd creature with white dot eyes, tiny thin legs,
blank serious expression. 小黑 must perform the core conceptual action, not decorate.

Theme: {主题}
Structure: {Workflow / 系统局部 / 前后对比 / 概念隐喻}
Core idea: {核心意思}
Composition: {小黑在哪里、正在做什么}
Labels: {标注词1} / {标注词2} / {标注词3}

Color: Black line art. Orange for flow. Red for key points. Blue for secondary notes.
Constraints: Main subject 40%-60%. At least 35% blank space. Max 5-8 labels.
```

---

### 3c. 极简线条（Minimal Line）

```text
Create a high-finish minimal line illustration about "{主题}".
Core concept: {视觉隐喻}
Visual language: Clean thin lines, selective vibrant color accents, strong negative space.
Composition: {构图}. Layers: main visual + auxiliary + annotation.
Title: "{标题}" integrated into composition.
Avoid: random decoration, generic abstract background, cluttered text.
```

---

### 3d. 产品手绘（Product Sketch）

```text
Create a 2K landscape product design sketch for "{产品}".
White sketch paper, industrial design process style.
{模式：3/4 perspective / exploded view / cutaway / ideation sheet}
Pencil, black fineliner, gray marker, construction lines, ellipses.
Annotations: {功能标注词}
Avoid photorealistic render, glossy 3D.
```

---

### 3e. 水彩手绘（Watercolor）

```text
Create a 2K transparent watercolor hand illustration of "{主题}".
Delicate ink contour, transparent blue-gray washes, pale beige tones.
Watery edges, pigment blooms, unfinished white margins.
Avoid photorealistic, glossy CGI, anime, flat vector.
```

---

### 3f. 建筑马克笔（Architectural Marker）

```text
Create a 2K architectural marker sketch for "{空间}".
Black fineliner, pencil construction, loose gray marker shadows.
Large white space. Expressive perspective, scale figures.
Avoid photorealistic arch-viz, CAD.
```

---

### 3g. 瑞士网格与维涅里标识（Swiss Modernist Grid）

```text
Create a high-resolution 2K image of "{主题}" in a strict Swiss Modernist poster style.
Off-white paper background (#f4f1ea) or pure white. Pure flat graphic design (no 3D/shadows).
Strict modular grid structure with visible column alignment.
Large bold sans-serif display lettering (Helvetica/Haas Grotesque feel) flush-left, ragged-right.
Maximum contrast of scale: very large title text vs very small labels.
Hairline rules and rulers (0.5–2pt) acting as strict structural anchors.
Accent color: A single bright identifier (e.g. Swiss Red #e4002b or Vermilion #f04e23) to denote structure/flow. Max 1 accent.
Avoid 3D, drop shadows, gradients, realistic textures, cluttered design, serif fonts.
```

### 3h. 编辑排版（Editorial Infographic）

**本质：瑞士国际排版风格信息图。** 严格三色、衬线大字、辐射布局、数据墨水比极高。参考「my second brain」类知识图。

```text
Create a {1600×450 banner / 1200×600 standard} editorial infographic in
Swiss International Typographic Style.

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
Core subject "{主题}" placed at visual center as hub node.
Spoke arms radiate outward to {6–12} satellite nodes.
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

Best model: Midjourney > Flux Dev > DALL-E 3
Aspect ratio: 1600×450 (banner landscape) or 1200×600 (standard)

Prohibited: gradients, drop shadows, >3 colors, rounded colorful bubbles,
hand-drawn strokes, AI art feel, glowing effects, dark background, icons with fill.
```

**子类型：**

| 子类型 | 场景 | 比例 | 节点数 |
|---|---|---|---|
| 知识系统图 | 个人系统/第二大脑/学习框架 | 1600×450 横幅 | 8–12节点 |
| 方法论图 | 工作流/决策框架/四象限 | 1200×600 | 6–8节点 |
| 对比信息图 | 两方案对比/before-after | 1200×600 | 双列各4节点 |

---

## [4] 出图

**主路径：直连 xAI（Grok），不经 Hermes。** 用本仓自带的零依赖脚本 `scripts/grok_image.py`。
密钥从环境变量 `XAI_API_KEY` 读，绝不写进命令行或落盘。

```bash
export XAI_API_KEY=...                      # 一次性，写进 shell/.env

# 单张：sketch 出 prompt → 管道 → 直连出图
archviz-sketch generate -s xiaohei --subject "三层架构循环" \
  | python3 scripts/grok_image.py --prompt-file - --out illustrations/01-xiaohei.jpg

# 或先存 prompt 再出图
python3 scripts/grok_image.py --prompt-file prompts/01.md --out illustrations/01.jpg --model grok-2-image

python3 scripts/grok_image.py --list-models     # 发现当前账号可用模型（别硬编码模型名）
```

模型默认 `grok-2-image`，可用 `--model` 覆盖（如 `grok-imagine-image-quality`）。

> 备选：若某项目仍配了 Hermes 的 `image_generate`，也可继续用；但本 skill 的默认与推荐是上面的直连脚本。

### 容错

| 错误 | 处理 |
|---|---|
| `XAI_API_KEY is not set` | 先 `export XAI_API_KEY=...` |
| `HTTP 401/403` | key 无效或额度问题 |
| `cannot reach api.x.ai` | 网络/代理不通（注意：Cowork 沙箱直连被挡，须在 host 终端跑） |
| API超时/限流 | 等10秒重试，最多2次 |

### 保存

每张图保存到 `{output-dir}/illustrations/01-{风格}-{主题}.png`

---

## [5] 视觉质检

用 `vision_analyze` 看图：

| 检查项 | 标准 | 不通过处理 |
|---|---|---|
| 构图 | 主体40-60%，留白≥35% | 改prompt |
| 主体动作 | 在做核心动作 | 改prompt |
| 标注文字 | ≤8处，2-8字/处 | 减少标注 |
| 色彩 | 克制，单色为主+点缀 | 加约束 |
| 风格一致 | 同批次统一 | 锁参数 |
| 画面干净 | 无渐变/阴影/噪点 | 加负面提示 |
| **过程稿特殊** ★ | 构造线可见、有涂改、不完美 | 加强草稿感 |

2轮后仍有问题：报告给用户。

---

## [6] 交付

```
{output-dir}/
├── strategy.yaml              # 配图策略
├── prompts/
│   ├── 01-过程稿-字体探索.md
│   └── ...
├── illustrations/
│   ├── 01-过程稿-字体探索.png
│   └── ...
└── report.md
```

---

## [7] 手绘风格图表 (Hand-drawn Charts)

交叉优化：archviz-sketch + archviz-diagram

**功能：** 将柱状图数据转换为手绘风格动画 GIF

**脚本：** `scripts/render_hand_drawn_chart.py`

**支持风格：**
- `xiaohei` — 小黑怪诞风格（纯白底、黑色线稿、红色点缀）
- `minimal-line` — 极简线条风格（细线、色彩点缀）
- `process-draft` — 过程稿风格（纸张纹理、草稿感）

**数据格式：**
```json
{
  "title": "Chart Title",
  "subtitle": "Description",
  "categories": ["A", "B", "C"],
  "values": [10, 20, 15],
  "labels": ["Label A", "Label B", "Label C"],
  "width": 800,
  "height": 500
}
```

**渲染命令：**
```bash
python3 scripts/render_hand_drawn_chart.py \
  --spec data.json \
  --outdir ./output \
  --basename chart-name \
  --style xiaohei \
  --frames 30 \
  --fps 15
```

**参数：**
- `--style`: 风格（xiaohei / minimal-line / process-draft）
- `--frames`: 帧数（默认 30）
- `--fps`: 帧率（默认 15）

**输出：**
- `chart-name.gif` — 动画
- `chart-name.png` — 静态图

**动画效果：**
- 柱状图从底部生长
- 手绘线条抖动效果
- ease-out 缓动函数

---

## 致谢与参考

本项目参考了以下开源项目：

| 项目 | 作者 | 借鉴内容 |
|---|---|---|
| [baoyu-article-illustrator](https://github.com/JimLiu/baoyu-skills) | 宝玉 (JimLiu) | 配图策略分析框架、Type×Style×Palette三维选型、prompt文件复用机制 |
| [ian-xiaohei-illustrations](https://github.com/helloianneo/ian-xiaohei-illustrations) | helloianneo | 小黑IP风格DNA、纯白手绘视觉规范、中文批注系统、构图约束 |
| [linear-concept-art-prompt](https://github.com/archsueh/linear-concept-art-prompt) | archsueh | 过程稿/作图痕迹风格、极简线条/产品手绘/水彩/建筑马克笔prompt模板 |

小黑（Xiaohei）是 helloianneo 创建的IP形象，本项目仅引用风格描述。

---

## 触发词

- "配图" / "插图" / "sketch" / "手绘"
- "过程稿" / "作图痕迹" / "草稿感" / "推演"
- "小黑风格" / "线条风格" / "水彩风格"
- "产品手绘" / "建筑手绘"
- "编辑排版" / "editorial" / "瑞士排版" / "信息图" / "infographic" / "奶油背景"
- "给文章加图"
