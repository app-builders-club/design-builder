# design-builder Plugin

This repository is a universal Claude Code and Codex plugin: `design-builder`. It bundles 6 slash commands, the `design` knowledge skill plus sister knowledge skills (`motion`, `playwright-cli`, `figma-use`), and the `design-auditor` sub-agent.

Manifests: `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. Portable entry: `skills/design-builder/SKILL.md`. Shared host rules: `references/host-compatibility.md`. Knowledge skill: `skills/design/SKILL.md`. Commands: `commands/`. Sub-agent: `agents/design-auditor.md`.

When the plugin is installed, users invoke commands as `/design-builder:<command>` — `setup`, `start` (alias of setup), `design_page`, `design_screen`, `build`, `improve`, `review`.

## Structure

- `.claude-plugin/plugin.json` — Claude Code manifest (name, version, mcpServers via `.mcp.json`, commands at `./commands/`)
- `.claude-plugin/marketplace.json` — single-plugin marketplace (so the repo itself is installable as a marketplace source)
- `.mcp.json` — shared MCP server config (`designlib` + `figma`)
- `commands/` — 6 user-facing commands: `setup.md`, `start.md` (alias), `design_page.md`, `design_screen.md`, `build.md`, `improve.md`, `review.md`
- `agents/design-auditor.md` — sole sub-agent. Used by `/review`. Returns P0-P3 report + JSON contract; supports `visual` / `code_only` / `mixed` modes; runs the AI-slop detector. Auto-captures running web apps via `playwright-cli` when the caller passes `urls`.
- `skills/design/SKILL.md` — knowledge skill: 3-layer model, Layer 2 filters (incl. Distinctiveness Gate), Layer 1 source order, `get_design_reference()` resolver (defined in `references/layer1-resolvers.md`), reference index.
- `skills/design/references/` — deep documentation (architecture, layer1-resolvers, inspiration_pages, commands, distinctiveness-gate, design-dials, designlib-mcp, ux-writing, web/, ios/, figma/, brand/, design/, slides/, system/, ui-styling/)
- `skills/design/data/` — CSV databases for BM25 search
- `skills/design/scripts/` — Python (search, design_system, system preview) + Node (anti-pattern detector). Stdlib only.
- `skills/design/templates/` — starters (iOS SwiftUI theme, brand-guidelines starter)
- `skills/motion/` — sister knowledge skill. Web-UI animation library knowledge (GSAP, WAAPI, CSS, Anime.js, Lottie, Three.js) + HyperFrames short-video pipeline. Loaded by `design` and the relevant commands.
- `skills/playwright-cli/` — sister knowledge skill. Browser automation via `@playwright/cli`. Used by `/review` (auto-screenshots of running web apps) and `/improve --restructure` (captures live inspiration_pages references). Runtime: `npx @playwright/cli`, no local install.
- `skills/figma-use/` — Figma Plugin API wrapper (mandatory prerequisite for any `use_figma` write).
- `NOTICE.md` — attribution for 6 source open-source projects + Figma MCP guide
- `LICENSE` — MIT
- `CHANGELOG.md` — version history

## Architecture (three-layer rule)

Every command must: (1) resolve facts through Layer 1 in the fixed order (project tokens → designlib MCP → local CSV → iOS HIG → free generation), via `get_design_reference(type, filters)`; (2) pass candidate output through all six Layer 2 filters (Direction, Dials, Aesthetics, Anti-Patterns, Distinctiveness Gate, Output Rules); (3) emit. Silently skipping Layer 2 is the #1 cause of generic "AI slop" output.

Extension markers in code: `KB-EXTENSION` (Layer 1 source), `FILTER-EXTENSION` (new Layer 2 filter). Pipeline markers from v1.2 are removed — there are no pipelines.

## The 6 commands at a glance

| Command                                | Output target                                          |
|----------------------------------------|--------------------------------------------------------|
| `/design-builder:setup`                | `<project>/design/design-system.md`, `style-guide.md`, `content-library.md`, `tokens.css`, `preview.html`, `references/`, `.cache/interview.json` |
| `/design-builder:design_page <name>`   | `<project>/design/pages/<name>.md` (web page spec, no code) |
| `/design-builder:design_screen <name>` | `<project>/design/screens/<name>.md` (iOS / native screen spec, no code) |
| `/design-builder:build [target]`       | Source code in user's source tree from a spec in `design/pages/` or `design/screens/` |
| `/design-builder:improve [target]`     | Patches user files via `Edit`; `--restructure` mode rebuilds sections from fresh anchors and may capture live inspiration_pages |
| `/design-builder:review [target]`      | `<project>/design/reviews/review-YYYY-MM-DD-HHMM.md` (delegates to `design-auditor`); accepts file path / Figma URL / HTTP(S) URL — URLs auto-captured via `playwright-cli` |

Every command ends with a `Next:` block recommending the next concrete action.

## inspiration_pages (new in v2.0)

Primary Layer 1 source for whole-page references. Query current records via `mcp__designlib__list_inspiration_pages` / `get_inspiration_page` / `list_inspiration_page_facets`. Schema map: `skills/design/references/inspiration_pages.md`. Resolver contract: `skills/design/references/layer1-resolvers.md`.

**Critical contract notes:**
- MCP filters are SINGULAR strings (one `mood`, one `signature`, one `keyword`). To combine values, call multiple times and dedupe by `id`.
- List response returns a SUBSET of fields; deep-fetch via `get_inspiration_page(page_id=<id>)` for full payload (palette, typography, sections, generation_prompt, why_it_works).
- The deep-fetch param is `page_id`, not `id`.
- inspiration_pages are **web-only**; iOS / cross requests fall back to `landing_patterns` or HIG.

Future: `inspiration_parts` (hero/CTA/paywall/pricing_table) — interface reserved in `MCP_TOOL_MAP`. Until then, partial-page references can be filtered today via `good_for_stage='hero_section' | 'cta_band' | ...` on inspiration_pages.

## Compatibility and validation

Keep native Claude commands and the auditor adapter. Codex enters via
`skills/design-builder/SKILL.md` and reads the same command recipes. Do not fork
workflow content by host. Preserve the shared MCP configuration and resolve plugin
resources independently of the user's working directory. Delegation is optional.

Python utilities and the Node detector's `--fast` mode require no third-party
packages. Browser capture, DOM/URL analysis and video workflows have optional
runtime dependencies; check live CLI help and installed versions.

Run `python3 scripts/validate_plugin.py` and
`python3 -m unittest discover -s skills/design/scripts -p 'test_*.py'`.
Validate Claude with `claude plugin validate .` and
`claude plugin validate .claude-plugin/plugin.json`.
For Codex, install the local marketplace and exercise `$design-builder` in a
separate fixture project, confirming it loads cached plugin files and writes only
project artifacts. Installation instructions are in README.md. Keep manifest
versions and changelog aligned; preserve LICENSE and NOTICE.md attribution.
