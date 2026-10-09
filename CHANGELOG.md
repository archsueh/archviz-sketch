# Changelog

## 0.1.1 (2026-10-09)

### Fixed

- **`references/` 里的两个文件谁也到不了。** SKILL.md 从头到尾没有出现
  `hand-drawn-sources.md` 或 `gotchas.md`，仓库里也没有别的文件引用它们 ——
  两个文件都存在、都写了内容，但 agent 永远不会知道它们存在。现已补一节
  `## 延伸参考 (References)` 索引表把两个都点名。这是套件新增的 `coverage`
  检查第一次派上用场的现场。
- **`scripts/` 有未声明的第三方依赖。** `render_concept_sketch.py` 与
  `render_hand_drawn_chart.py` 顶层 `import PIL`，而仓库既无 `requirements.txt`，
  pyproject 的 `dependencies = []` 又是刻意的（包本身零依赖）。现由
  `requirements.txt` 声明 Pillow，并由套件的 `deps` 检查守住不再复发。
  同一缺陷在**家族五个仓库里全部存在**。

### Added

- **`## 延伸参考 (References)`** —— 本仓第一个真正的 references 索引。
- **`requirements.txt`** —— `Pillow`。此前干净检出直接 `ImportError`。
- **`coverage` 检查** —— 套件新增：`references/*.md` 必须从 SKILL.md **可达**。
  索引里漏一个文件，任何计数都还是对的 —— 这个失效模式 `counts` 结构上看不见。
- **`deps` 检查** —— 套件新增：把仓库里每个第三方 import 与清单对账。

### Changed

- **`design-judgment` 集成块移出 SKILL.md 正文。** 2026-10-09 20:32:55 有并行会话
  在五个 archviz 仓库的 SKILL.md 末尾各追加了一段 956 字节的
  `<!-- design-judgment-integration -->` 块（交付前跑五段判断链自检）。
  **内容逐字保留，未删改一字**，但 956 字节会把本仓顶到 20,349 / 20,000 —— 超限。
  现移入 `references/design-judgment.md`，正文只留一行指针，SKILL.md 回到
  19,759 字节。

## 0.1.0 (2026-10-09)

This repo had **no CI** before this release, and its style count was wrong in
three places at once. Both are now gated.

### Fixed

- **`pyproject.toml` was 0.0.2 while SKILL.md and CHANGELOG said 0.0.4.**
  `pip install -e .` would have installed a package whose metadata reported a
  version the skill never shipped. SKILL.md `metadata.version` is the release
  truth; everything else is now checked against it.
- **The style count was wrong: docs said 8, the code has 7.** Corrected in
  SKILL.md (both occurrences) and in the 0.0.4 entry below, which also claimed
  "Eight in-skill templates".
- **`description` named none of the seven style ids.** It listed Chinese trigger
  words (`过程稿`, `小黑风格`) but not one machine-readable id, so
  "画个 watercolor 风格" had no lexical hook. All seven ids are now named, each
  with its Chinese equivalent — the description is the one text an agent reads
  *before* deciding to load the skill.

### Added

- **`scripts/check_archviz.py`** — the family's portable consistency kit
  (archviz-diagram ADR-003). One file, per-repo `archviz-checks.json`, stdlib
  only, no venv and no package import required. Five checks: `version` /
  `budget` / `routing` / `counts` / `cjk`. `--self-test` carries 23 adversarial
  fixtures, four of which must **not** fire.
- **`.github/workflows/ci.yml`** — first CI for this repo: runs the kit, then
  the kit's own checker.
- **`scripts/git-pre-commit.sh`** — the same gates locally.
- **`.gitattributes`** — pins SKILL.md to LF; the byte cap counts LF-normalised
  bytes.
- **`archviz-checks.json`** — two count claims, not one:
  1. the declared style count == `STYLE_REGISTRY` length (7);
  2. the number of **implemented** rows in SKILL.md's 风格总览 table == 7.

  The second exists because the table carries one row (`编辑排版`) that no
  registry entry, prompt template, demo, README or reference backs. It is now
  marked `⛔ 未实现` in the table so the document stops promising what the code
  cannot do. The check excludes marked rows, so the gate holds the implemented
  count without deleting a genuine design intention.

### Notes

- **`编辑排版` is not implemented, and never was.** `git log --diff-filter=A --
  templates/prompts/` shows exactly seven templates have ever been added. The
  row is kept — it is a real design intention — but it is labelled, and it is
  not counted as shipped. Whether to implement it or drop it is an open decision.
- The 0.0.4 entry's "Eight in-skill templates" is corrected in place with a
  dated note rather than silently rewritten: the entry is a record of what was
  believed then, and the correction is part of the record.

### Verified

- `scripts/check_archviz.py` → PASS (5/5)
- `scripts/check_archviz.py --self-test` → 23/23
- The version check caught the pyproject drift on its first run, before it was
  fixed — the gate is load-bearing, not decorative.

## 0.0.4 (2026-09-14)

### Added
- Route numbered hand-drawn styles (`041号`, 手绘风格库, gallery browse) to sidecar skill `handdraw-style-prompter` (yang0/handraw-style). Seven in-skill templates unchanged.

  > **Correction (2026-10-09):** this line originally read "Eight in-skill
  > templates" and has been corrected to **Seven**. The repository has always
  > had seven — `templates/prompts/` and `git log --diff-filter=A --
  > templates/prompts/` both show seven, and the eighth (`编辑排版`) was never
  > implemented. It existed only as a row in SKILL.md's style table, which is
  > now marked `⛔ 未实现`. The number is corrected in place with this dated
  > note rather than silently, so the record of what was believed then survives.
- Reference-image isolation when a numbered style image is used: borrow line/medium/color only, never subject or composition.
- Credit yang0/handraw-style in the acknowledgements table.

## 0.0.2 (2026-06-14)

### Fixed
- **Parameter injection was dead.** Templates used single-brace Chinese placeholders (`{主题}`) while the engine only replaced `{{key}}`, so `params` were never substituted and the MCP/CLI always returned the raw template. Primary subject slot in all 4 original templates normalized to `{{subject}}`; engine now substitutes both `{{key}}` and `{key}`.

### Added
- **watercolor** and **architectural-marker** prompt templates + registry entries. The registry/MCP/CLI now actually expose all 6 styles the docs advertised (previously only 4 were reachable in code).
- `scripts/grok_image.py` — zero-dependency (stdlib only) direct xAI/Grok image generator. Reads `XAI_API_KEY` from env, posts to `/v1/images/generations`, runtime model discovery via `--list-models`, stdin pipe from `archviz-sketch generate`. Removes the Hermes `image_generate` dependency; SKILL.md §[4] updated to make this the default path.

### Changed
- `archviz_sketch_generate` description now states it returns a PROMPT, not an image, and points to a configured image-generation tool (Grok/FAL/OpenAI) for the actual render. API keys stay in that tool's config.
- Corrected the `xiaohei` style description (pure white ground + black line art, not "warm tones").

## 0.0.1 (2026-06-12)

**Initial release**

### Added
- 6 illustration styles: process draft, Xiaohei, minimal line, product sketch, watercolor, architectural marker
- Content analysis → strategy → prompt → generation → QA → delivery pipeline
- Process draft sub-types: ballpoint, typography, product sketch, design iteration
- Annotation vocabulary system (design/typography/general)
- Visual QA checklist with vision_analyze integration
- API-agnostic design (supports FAL/OpenAI/xAI)
