# design-builder

**Production-grade UIs from Claude Code and Codex — without the AI-slop look.**

A shared design plugin for Claude Code and Codex that turns AI-generated UI from "obviously AI" into something you'd actually ship. Real references, layered filters, spec-first workflow.

→ [Quickstart](#quickstart) · [The 6 commands](#the-6-commands) · [How it works](#three-layer-architecture)

| Command | What it does | When to use |
|---|---|---|
| `/design-builder:setup` (alias `start`) | Interview → reference discovery → 2-3 direction candidates → HTML preview → emit `design-system.md`, `style-guide.md`, `content-library.md`, `tokens.css`, `preview.html`. | New project. You don't have a design foundation yet. |
| `/design-builder:design_page <name>` | Reads the foundation → pulls inspiration_pages → user picks → writes a design spec to `design/pages/<name>.md` (no code). | You want to plan a web page before shipping code. |
| `/design-builder:design_screen <name>` | Same, for app screens. Uses landing_patterns + iOS HIG. Spec adds Navigation context, Gestures, Safe areas. Writes to `design/screens/<name>.md`. | You want to plan an iOS / native screen before shipping code. |
| `/design-builder:build [target]` | Reads spec(s) from `design/pages/` and/or `design/screens/` → writes code to your source tree. Supports single (`build landing`), batch (`build all`), glob, or interactive multi-select. | After one or more specs exist and you want production code. |
| `/design-builder:improve [target]` | Light audit of code / Figma / screenshots → list of concrete fixes → apply mechanical ones (`Edit`). `--restructure` mode rebuilds weak sections from a fresh `inspiration_pages` anchor and can capture the live reference page via `playwright-cli`. | Existing design. Something feels off. You want quick wins. |
| `/design-builder:review [target]` | Strict critique by `design-auditor` agent: composition, typography, color/WCAG, motion, AI-slop, anti-patterns, accessibility. P0-P3 report → `design/reviews/`. Accepts file path / Figma URL / **HTTP(S) URL** — URLs are auto-captured at desktop + mobile via `playwright-cli`. | Before shipping, or when `/improve` finished and you want full validation. |

## The problem we keep hitting

Ask Claude Code to design a UI. You get the same purple-to-pink gradient, the same generic card layout, the same "modern minimal" spacing every other AI-coded site has. The output isn't *bad* — it's median. And median is identifiable on sight.

The reason isn't model capability. It is missing inputs:

- No real design references — agents guess hex codes and font pairings
- No filters between concept and code — slop ships unedited
- No separation between *design* and *implementation* — every change re-rolls the dice

`design-builder` fixes the inputs.

---

## What sets it apart

**Real references, not vibes.** `inspiration_pages` sourced from land-book, served via the `designlib` MCP — full pages with palette, typography, sections, mood, and generation prompt. Specs pull from these instead of inventing.

**Six layered filters.** Every command's output is gated through Direction → Dials → Aesthetics → Anti-Patterns → **Distinctiveness Gate** → Output Rules before emit. The Distinctiveness Gate catches most "looks AI-generated" outputs before they reach code.

**Spec-first.** `/design_page` and `/design_screen` write a markdown design spec. `/build` vendors that spec into source code. The spec is the contract — change the spec, regenerate the code.

**Shared audit workflow.** `/review` runs inline or through Claude's `design-auditor` adapter, which loads a11y / perf / HIG / motion / anti-pattern references, runs WCAG checks, and returns a structured P0-P3 report.

---

## Quickstart

### Claude Code

Install from a local checkout (includes unpublished changes):

```text
/plugin marketplace add /absolute/path/to/design-builder
/plugin install design-builder@design-builder-marketplace
```

Or install the published GitHub version:

```
/plugin marketplace add app-builders-club/design-builder
/plugin install design-builder@design-builder-marketplace
```

Then in any project:

```
/design-builder:setup
```

That is it. The interview produces 2-3 direction candidates, you pick one, and you have a design foundation in `design/`. From there:

- **Web page** → `/design-builder:design_page <name>` → `/design-builder:build <name>`
- **iOS screen** → `/design-builder:design_screen <name>` → `/design-builder:build <name>`
- **Existing surface** → `/design-builder:improve` or `/design-builder:review`

### Codex

```sh
codex plugin marketplace add /absolute/path/to/design-builder
codex plugin add design-builder@design-builder-marketplace
```

Start a new Codex session to refresh available skills, then use:

```text
$design-builder setup
$design-builder design_page landing
$design-builder build landing
$design-builder review src/
$design-builder improve src/
```

The same six workflow files serve both hosts. Claude retains its native commands
and auditor adapter; Codex can execute the audit inline. The `design`, `motion`,
`playwright-cli` and `figma-use` knowledge skills remain bundled.

Local Python search, previews and contrast checks use the standard library.
The Node detector supports dependency-free `--fast` analysis. Optional browser
capture uses `@playwright/cli` (0.1.23 declares Node >=18); video uses HyperFrames
(0.8.225 declares Node >=22). Verify installed versions and browser availability.
MCP integrations are optional and may require authentication. No duplicate global
MCP registration is needed when the host has loaded the plugin's `.mcp.json`.

---

## The 6 commands

| Command | What it does | When to use |
|---|---|---|
| `/design-builder:setup` (alias `start`) | Interview → reference discovery → 2-3 direction candidates → HTML preview → emit `design-system.md`, `style-guide.md`, `content-library.md`, `tokens.css`, `preview.html`. | New project. You do not have a design foundation yet. |
| `/design-builder:design_page <name>` | Reads the foundation → pulls inspiration_pages → user picks → writes a design spec to `design/pages/<name>.md` (no code). | You want to plan a web page before shipping code. |
| `/design-builder:design_screen <name>` | Same, for app screens. Uses landing_patterns + iOS HIG. Spec adds Navigation context, Gestures, Safe areas. Writes to `design/screens/<name>.md`. | You want to plan an iOS / native screen before shipping code. |
| `/design-builder:build [target]` | Reads spec(s) from `design/pages/` and/or `design/screens/` → writes code to your source tree. Single (`build landing`), batch (`build all`), glob, or interactive multi-select. | After one or more specs exist and you want production code. |
| `/design-builder:improve [target]` | Light audit of code / Figma / screenshots → list of concrete fixes → apply mechanical ones (`Edit`). | Existing design. Something feels off. You want quick wins. |
| `/design-builder:review [target]` | Strict critique by `design-auditor` agent: composition, typography, color/WCAG, motion, AI-slop, anti-patterns, accessibility. P0-P3 report → `design/reviews/`. | Before shipping, or when `/improve` finished and you want full validation. |

Every command ends with a `Next:` block telling you what to do next.

---

## Project output — `design/` folder

`/setup`, `/design_page`, `/design_screen`, `/build`, and `/review` write to `<your-project>/design/`:

```
design/
  design-system.md     # palette, typography, spacing, mood, anti-patterns
  style-guide.md       # a11y floor, platform constraints, density, motion, states
  content-library.md   # voice & tone, UI states, forms, notifications
  tokens.css           # CSS variables (or tokens.json for non-web)
  preview.html         # visual preview of the system / page
  pages/               # design specs for web pages (markdown), one per page
  screens/             # design specs for app screens (markdown), one per screen
  references/          # your reference URLs + downloaded screenshots
  screenshots/         # drop screenshots here for /review — OR pass a URL and playwright-cli auto-captures here at 1440x900 + 375x812
  reviews/             # P0-P3 audit reports (review-YYYY-MM-DD-HHMM.md)
  .cache/              # debug context for cross-command state (gitignored — interview.json, stack.json, inspiration/<page_id>.png, ...)
```

**Recommended `.gitignore`:**

```
design/references/downloaded/
design/screenshots/
design/.cache/
```

Version `design-system.md`, `style-guide.md`, `content-library.md`, `tokens.css`, `pages/`, `screens/`, `reviews/`. The downloaded binaries and `.cache/` debug state are noise.

---

## Three-layer architecture

```
COMMANDS         →  /setup · /design_page · /design_screen · /build · /improve · /review
SKILL (rules)    →  Layer 2 filters · Layer 1 resolvers · knowledge base
LAYER 1 SOURCES  →  Project tokens · designlib MCP (inspiration_pages, palettes, ...) · CSV · iOS HIG · free
```

Every command's output is gated through six Layer 2 filters before emit. Skipping Layer 2 = AI slop.

Detail: [`skills/design/references/architecture.md`](skills/design/references/architecture.md).

---

## inspiration_pages — the whole-page reference

`designlib` MCP exposes `inspiration_pages` (sourced from land-book): full-page references with palette / typography / sections / mood / generation_prompt. `/design_page` uses them as the primary seed for new page specs; `/build` then vendors the spec into code. Future: `inspiration_parts` (hero / CTA / paywall / pricing_table) — interface reserved.

- Schema map: [`skills/design/references/inspiration_pages.md`](skills/design/references/inspiration_pages.md)
- Resolver contract: [`skills/design/references/layer1-resolvers.md`](skills/design/references/layer1-resolvers.md)

---

## Sub-agent: `design-auditor`

`/review` executes [the shared audit](skills/design/references/audit-workflow.md). Claude can delegate through `agents/design-auditor.md` when permitted; Codex runs the same dimensions and report contract inline.

The audit covers: composition, hierarchy, focal point, rhythm, grid, typography, color, WCAG, motion, **AI-slop detector** (Distinctiveness Gate's 7 questions applied to as-built surfaces), anti-patterns, accessibility. iOS adds Dynamic Type AX5, Reduce Motion, Increase Contrast/Transparency, accessibility labels, HIG checks.

If no visual is available, the auditor runs in **code-only mode** and explicitly flags that composition / focal point / rhythm / mood-fit were not evaluated. To skip the manual screenshot step, pass an HTTP(S) URL to `/review` and the auditor auto-captures via `playwright-cli` (see below).

## Motion — animation knowledge & short-video

The `motion` knowledge skill (`skills/motion/SKILL.md`) is the sister of `design`. It owns *how* animation gets implemented — the `design` skill picks the candidate, `motion` writes correct code. Two modes:

- **Web-UI mode.** Per-library production knowledge: GSAP, WAAPI, CSS, Anime.js, Lottie, Three.js. Includes a selection decision matrix (`references/selection.md`), `prefers-reduced-motion` patterns for each library, bundle-cost guidance, and the P0–P3 anti-patterns checklist consumed by the auditor's Motion dimension and `/improve` Phase 2 step 5. `/build` routes hand-rolled animations through this skill so every emit respects accessibility and performance rules.
- **Video mode.** Short-video generation via the HyperFrames pipeline (HTML compositions seeked frame-by-frame, FFmpeg encode). Composition contract + CLI commands (`init / lint / inspect / preview / render / transcribe / tts`) + Tailwind v4 browser runtime notes. Activated when the user asks for an MP4 / WebM deliverable rather than UI motion.

Anti-pattern catalog: [`skills/motion/references/anti-patterns.md`](skills/motion/references/anti-patterns.md). Library reference index: [`skills/motion/SKILL.md`](skills/motion/SKILL.md).

## Live web capture — `playwright-cli`

The `playwright-cli` knowledge skill (`skills/playwright-cli/SKILL.md`, vendored from `@playwright/cli`, Apache-2.0) gives the plugin browser-automation muscle without a manual screenshot loop. Two integration sites today:

- **`/review` with a URL.** `/design-builder:review http://localhost:3000` (or `https://example.com,https://example.com/pricing`) captures each URL at desktop (1440×900) + mobile (375×812), drops PNGs into `design/screenshots/<slug>.<viewport>.png`, then runs visual mode. Replaces the v2.0 "drop screenshots manually" stub for web targets.
- **`/improve --restructure` with a fresh `inspiration_pages` anchor.** When the chosen anchor has a `url`, the live page is captured to `design/.cache/inspiration/<page_id>.png` (gitignored, reused on subsequent runs) so the rebuild plan can reference real composition rather than only metadata.

Runtime is `npx @playwright/cli` — no global install, no `npm install` step. The first call downloads on demand. If unavailable (offline, no Node), capture steps fall back gracefully and the auditor surfaces a Caveats line. Mobile / iOS captures are still manual (Playwright doesn't help there).

---

## Figma integration

The Figma MCP (`https://mcp.figma.com/mcp`) ships pre-configured. When connected, the plugin routes Figma URLs:

- `/improve <figma-url>` → reads design context + screenshot, applies requested edits when the connected write tool and file permissions allow them; otherwise reports a concrete patch plan.
- `/review <figma-url>` → uses Figma as the visual source for the audit.

Routing detail: [`skills/design/references/figma/README.md`](skills/design/references/figma/README.md). Requires authenticated Figma MCP. Writing to canvas is available through `use_figma` for supported clients/plans with edit access; inspect the actual tool schema. See [current Figma write access](https://developers.figma.com/docs/figma-mcp-server/write-to-canvas/) and [rate limits](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/). Limits govern reads differently from writes; do not assume a fixed monthly quota.

---

## What's inside

- `commands/` — 6 user-facing slash commands (+ `start.md` alias for `setup`)
- `skills/design/SKILL.md` — knowledge base, filters, Layer 1 resolvers
- `skills/design/references/` — deep documentation (web, iOS, motion, brand, figma, system, ui-styling, slides)
- `skills/design/data/` — CSV databases (UX guidelines, tech stacks, anti-patterns)
- `skills/design/scripts/` — BM25 search (Python), design system generator (Python), anti-pattern detector (Node.js)
- `skills/design/templates/` — starters (iOS SwiftUI theme, system preview, brand guidelines)
- `skills/motion/` — sister knowledge skill: web-animation libraries (GSAP/WAAPI/CSS/Anime/Lottie/Three) + HyperFrames short-video pipeline
- `skills/playwright-cli/` — sister knowledge skill: browser automation for `/review` URL captures and `/improve --restructure` live inspiration_pages
- `skills/figma-use/` — Figma Plugin API wrapper (mandatory prerequisite for any `use_figma` write)
- `agents/design-auditor.md` — sole sub-agent (used by `/review`)
- `skills/design-builder/SKILL.md` — portable task router
- `.claude-plugin/` — Claude Code manifest + marketplace
- `.codex-plugin/` and `.agents/plugins/` — Codex manifest + marketplace
- `references/host-compatibility.md` — shared host adapter
- `.mcp.json` — `designlib` + `figma` MCP server config

---

## Optional: install `designlib` MCP standalone

Pre-configured in `.mcp.json`. To install standalone:

```
claude mcp add --transport http designlib https://designlib.app-builders.club/mcp
```

Without it, the plugin uses project tokens, local CSV and platform references. Remote landing patterns, inspiration pages and animation recipes are unavailable; freely generated substitutes are labeled as such. Catalog counts are discovered live.

---

## Part of App Builders Club

`design-builder` is one of three open-source tools we ship for builders who code with AI:

- **[mvp-builder](https://github.com/app-builders-club/mvp-builder)** — Document-Driven Development for Claude Code. Specs before code, TDD enforced, self-review catches stubs.
- **design-builder** — this repo. Production-grade UIs without the AI-slop look.
- **[designlib-mcp](https://github.com/app-builders-club/designLib-mcp)** — the design-knowledge MCP that powers design-builder. Works standalone in any MCP client.

Methodology and build films at [app-builders.club](https://app-builders.club)

---

## Credits

Built on top of five open-source projects: [Impeccable](https://github.com/pbakaus/impeccable), [Emil Kowalski Design Skill](https://emilkowal.ski/skill), [Taste Skill](https://github.com/Leonxlnx/taste-skill), [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), and [Design Motion Principles](https://github.com/kylezantos/design-motion-principles). See [NOTICE.md](NOTICE.md).

## License

MIT. See [LICENSE](LICENSE).
## Compatibility and validation

See [host rules](references/host-compatibility.md) for tool discovery, path resolution
and offline behavior. Validate a checkout with `python3 scripts/validate_plugin.py`
and `python3 -m unittest discover -s skills/design/scripts -p 'test_*.py'`.

Packaging and runtime guidance checked on 2026-11-01 against
[Claude plugin reference](https://code.claude.com/docs/en/plugins-reference),
[Codex plugin packaging](https://developers.openai.com/plugins/build/plugins),
[Playwright CLI](https://github.com/microsoft/playwright-cli), and
[HyperFrames](https://github.com/heygen-com/hyperframes).
