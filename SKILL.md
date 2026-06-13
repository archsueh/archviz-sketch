---
name: archviz-sketch
description: |
  当用户需要为文章、教学材料或概念方案配“过程稿、手绘概念图、带明显作图痕迹的线稿/插图”时加载。
  核心差异化：保留构造线、草稿感、不完美的手作能量（过程稿/作图痕迹）。
  6种风格（过程稿★、小黑怪诞、极简线条、产品手绘、水彩手绘、建筑马克笔）。
  需要 image_generate 工具（用户自行配置 API）。
  2D 数据可视化（图表、流程图）→ archviz。
  3D 空间可视化 → archviz-3d。
license: MIT
metadata:
  version: 0.1.0
  source: https://github.com/archsueh/archviz-sketch
  risk: safe
  author: archsueh
  triggers: 配图, 插图, sketch, 手绘, 过程稿, 作图痕迹, 草图, 生草图, 线稿, 概念图, concept art, process drawing, hand-drawn
---

# archviz-sketch

> 文章配图全流程管线。**核心差异化：过程稿/作图痕迹**——保留构造线、草稿感、不完美的手作能量。

## When to Use
- 文章/教学/概念内容需要“正在画”的手绘感插图
- 需要过程稿、字体探索、产品/建筑手绘、带标注的线条艺术
- 追求不完美手作痕迹而非干净成品

## When NOT to Use
- 2D 数据图表、流程图、架构图、编辑卡片 → **archviz**
- 3D 建筑/机械结构可视化 → **archviz-3d**
- 摄影级或纯矢量成品图 → imagegen / fal MCP（或 archviz 2D）

## Skill Boundaries
| Need                  | Use            |
|-----------------------|----------------|
| 2D diagram / chart    | archviz        |
| 3D spatial / exploded | archviz-3d     |
| Hand-drawn / 生草图   | **this skill** |

## Architecture (Guizang Fat Skill)
- SKILL.md（本文件）：短路由 + 核心判断
- references/：hand-drawn-sources、styles/、quality-checklist、gotchas（最高价值）
- templates/prompts/ + styles/：6 风格精确模板 + 负面约束
- 真实任务驱动 → 视觉质检 → 追加 gotchas → 内容反馈循环

## Key Constraints (Taste as Explicit Rules)
- 过程稿必须可见构造线、压力不均、涂改痕迹、留白 ≥35%
- 标注 ≤8 处，2-8 字/处
- AI 图仅兜底；优先真实摄影/手绘参考
- 负面提示强制：clean vector, perfect alignment, glossy, photoreal, no construction lines

## Status
YOLO 执行中。已迁移老 sketch-pipeline 核心 workflow + templates。正在填充 400-free hand-drawn sources + 真实使用 gotchas。

## License
MIT
