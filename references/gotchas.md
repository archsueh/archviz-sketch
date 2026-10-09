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

---

## 2026-10-09 — 风格计数漂移与孤儿行

- **文档说 8 种风格，代码给 7 —— 且「8」这个数字在 CHANGELOG 里也出现过。** SKILL.md 两处写「8种风格」，0.0.4 的 CHANGELOG 条目写「Eight in-skill templates」。实测：`STYLE_REGISTRY` 7 个顶层条目、`templates/prompts/` 7 个文件、`list_styles()` 返回 7 个。**计数错在文档侧，不是代码侧。** 参考 archviz-diagram 的「调色板数量别写死」（11 写成 4）与「类型数别写死」（13 写成 14）—— 同型，第三次。**纪律：任何要写进文档的计数，落笔前跑一次命令取真值；取不到就写「见 XXX 注册表」，不要给数。**

  > **补充（2026-10-09）**：上面说「SKILL.md 两处」，实际是**三处**。当时修的是 §风格总览的
  > 「8种风格」和 description 里的同名计数，**漏了「和 handdraw-style-prompter 分流」表里的
  > 「8 套模板」** —— 那一行不在 `counts` 的任何断言里，所以闸门也看不见它。现在改成 7，并且
  > 把 `(\d+)\s*套模板` 加进了 `counts`（真值 = `templates/prompts/*.md` 的 glob 计数）。
  > 教训不是「数错了」，是**「修完要全仓 grep 那个数」** —— 一处断言只锁一处文本。

- **`编辑排版` 是孤儿行：文档承诺了、代码给不出。** 它只出现在 SKILL.md 的「风格总览」表里，`STYLE_REGISTRY` 无条目、`templates/prompts/` 无模板、`demo-styles.html` / `README` / `CHANGELOG` / `references/` 全都没有它。`git log --diff-filter=A -- templates/prompts/` 显示**历史上只添加过 7 个模板**，从未有过第 8 个 —— 所以这句「Eight」在当时就是错的。**处置：不删行**（它是真实的设计意图），改为标注 `⛔ 未实现`，并让计数闸门**排除带标注的行**。**这是 archviz-diagram `blueprint` 调色板 bug 的同型**：一个东西到了文档却从未到代码，且没有任何东西能发现。**判据：新增风格/类型/调色板时，先确认它同时出现在 ① 注册表 ② 资源目录 ③ 示例页 —— 三处缺一即为未实现，不要写进面向用户的表。**

  > **处置已更新（2026-10-10）：改为接线实现，不再标注「未实现」。** 判据是成本与能力的实测，
  > 不是偏好：① prompt 已完成且与 §3a–3g 同构（本质一句 → ` ```text ``` ` 块 → 子类型表，55 行）；
  > ② 接线成本 = `STYLE_REGISTRY` 1 条 + `templates/prompts/editorial-infographic.md` 1 个；
  > ③ 丢弃反而更贵 —— 要删 §3h、风格总览行、风格自动推荐行、分流表提及、触发词行共 5 处，
  > 并失去家族里唯一覆盖「知识系统 / 第二大脑信息图」体裁的风格。**与 `swiss-modernist` 不重复**：
  > 后者是无衬线海报（grid + 单点缀色），本风格是衬线大标题 + 严格三色 + 辐射布局的信息图。
  > 真值 7 → 8，三处计数断言与 `templates/prompts/*.md` 的 glob 同步。
  >
  > **同时更正本条里的一个判据错误。** 原文把「③ 示例页」也当成必需，三处缺一即为未实现。
  > 实测（2026-10-10）：7 个已实现风格里，`demo-styles.html` 只有 `xiaohei` 一个，`demo.html`
  > 只有 3 个，`README.md` **一个都没有**。所以「示例页收录」**不是**实现与否的判据 —— 真正的
  > 判据只有两处：① `STYLE_REGISTRY` ② `templates/prompts/`。示例页是可选门面，不是契约。
  >
  > **半接线（进了文档、没进引擎）才是真故障**，不是文案瑕疵：`list_styles()` 不返回它，
  > `mcp_server.py` 也不暴露它，agent 照 §3h 出图会拿到 `ValueError: Unknown style`。
  > `routing` 闸门现在保证这种状态不可能再发生 —— registry 里每个 id 都必须出现在
  > `description` 里，加了条目却忘了路由面会直接 FAIL（本轮实测 8/8 命中）。

- **路由面要写机器可读的 id，不能只写中文别名。** `description` 原先列了「过程稿、小黑风格、线条艺术」等中文触发词，但**一个 style id 都没有** —— 用户说「画个 watercolor 风格」时没有词法钩子。现在 7 个 id 全部点名，各带中文对应词。**中文别名走子串匹配、ASCII id 走词边界**（`\b手绘\b` 匹配不到「手绘风格」，所以 CJK 不能用词边界）。
