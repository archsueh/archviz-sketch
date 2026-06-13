# Gotchas (Highest Value — From Real Failures)

## Process-Gao / 过程稿
- 模型会自动“干净化”：必须在 prompt + negative 里双重锁死 “visible construction lines, pressure variation, eraser ghosts, side trials, crossed-out attempts”。
- CJK 标注容易完美对齐而失去手感：强制 “handwritten wobbly Chinese annotations, inconsistent pressure”。

## 风格一致性
- 多图 batch 时风格漂移严重：先锁一个 reference image + 详细 Visual DNA，再生成 batch。
- 小黑 IP 容易被模型“可爱化”：严格 “blank serious expression, tiny thin legs, no smile, absurd creature”。

## 质检失败常见
- 构图主体 <40% 或 >60%：策略阶段必须计算主体占比。
- 标注太多 (>8)：策略 yaml 里硬上限。
- 真实摄影兜底时边缘太锐：加 “soft natural photo edges, slight grain”。

## 交付
- 用户期望“成品”而非“过程”：在 strategy 阶段明确沟通“这是草稿感，不是最终渲染”。
- 导出后在 Obsidian/PPT 里线条发虚：生成时强制 2K+ 分辨率 + 后期锐化 checklist。

**持续追加**：每次真实使用后至少加 1 条。优先负面边界。
