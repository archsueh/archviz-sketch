# Changelog

## 0.0.2 (2026-06-14)

### Fixed
- **Parameter injection was dead.** Templates used single-brace Chinese placeholders (`{主题}`) while the engine only replaced `{{key}}`, so `params` were never substituted and the MCP/CLI always returned the raw template. Primary subject slot in all 4 original templates normalized to `{{subject}}`; engine now substitutes both `{{key}}` and `{key}`.

### Added
- **watercolor** and **architectural-marker** prompt templates + registry entries. The registry/MCP/CLI now actually expose all 6 styles the docs advertised (previously only 4 were reachable in code).

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
