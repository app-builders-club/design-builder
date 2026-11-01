# Design Builder

**Design systems, web pages and iOS screens for Claude Code and Codex.**

Use the same agent for design and implementation. Design Builder helps you choose a visual direction, turn it into a reusable design system, specify pages and screens, and build them in your project. Reviews check the result against the design intent, accessibility requirements and platform conventions.

Built for indie founders, frontend developers and designers who code. Works with web projects such as Astro, Next.js, Vite and plain HTML, and with SwiftUI on iOS.

[Product page](https://app-builders.club/tools/design-builder/) · [Quickstart](#quickstart) · [Commands](#commands) · [License](LICENSE)

## How it works

Start with your brief and any existing brand assets or project tokens. For a new direction, Design Builder proposes candidates and renders an HTML preview so you can choose visually. Once the foundation is in place, page and screen specifications capture the layout, content and interactions before implementation.

The design checks cover typography, color, spacing, motion, accessibility and recurring generic UI patterns. Existing project decisions carry through the workflow. A small fix or review can start directly from the code without a new design interview.

## Quickstart

### Claude Code

Run these commands inside Claude Code:

```text
/plugin marketplace add app-builders-club/design-builder
/plugin install design-builder@design-builder-marketplace
```

Restart Claude Code, open your project, then run:

```text
/design-builder:setup
```

To install a local checkout, use its absolute path in the marketplace command:

```text
/plugin marketplace add /absolute/path/to/design-builder
/plugin install design-builder@design-builder-marketplace
```

### Codex

Clone the repository, then register and install the plugin from your terminal:

```sh
git clone https://github.com/app-builders-club/design-builder.git
codex plugin marketplace add "$(pwd)/design-builder"
codex plugin add design-builder@design-builder-marketplace
```

If you already have a checkout, use its absolute path with `codex plugin marketplace add`.

Open a new Codex chat in your project and write:

```text
Use Design Builder to set up the design system for this project.
```

You can also invoke the skill explicitly:

```text
$design-builder setup
```

The `$` prefix selects a skill in Codex; it is not a terminal command. Both agents use the same workflows and design knowledge.

## Commands

| Action | What it produces | Claude Code | Codex |
|---|---|---|---|
| Set up | Design foundation, tokens and HTML preview | `/design-builder:setup` | `$design-builder setup` |
| Plan a web page | Specification in `design/pages/` | `/design-builder:design_page landing` | `$design-builder design_page landing` |
| Plan an app screen | Specification in `design/screens/`, including navigation, gestures and safe areas | `/design-builder:design_screen settings` | `$design-builder design_screen settings` |
| Build | Implementation from the selected specification | `/design-builder:build landing` | `$design-builder build landing` |
| Improve | Targeted fixes to an existing interface | `/design-builder:improve src/` | `$design-builder improve src/` |
| Review | Prioritized findings in `design/reviews/` | `/design-builder:review src/` | `$design-builder review src/` |

`start` is an alias for `setup`. Build accepts a single target, all specifications or a pattern. Use `improve --restructure` when a section needs a different composition.

For a new web page, follow `setup → design_page → build → review`. For an existing interface, start with `improve` or `review`.

## Design references

The bundled knowledge includes palettes, font pairings, styles, UX guidance, stack-specific advice and iOS Human Interface Guidelines. When the hosted design library is available, the plugin can also retrieve curated page references and animation recipes.

The plugin works with project tokens and bundled data when the hosted library is unavailable. Remote references are then unavailable, and generated alternatives are identified as such.

## Review an existing interface

Review a file or directory, supply screenshots, or pass a running page URL:

```text
/design-builder:review http://localhost:3000
```

In Codex:

```text
$design-builder review http://localhost:3000
```

With browser capture available, the review can inspect desktop and mobile views. Without visual evidence, it performs a code-only review and identifies which visual qualities could not be assessed. Findings use P0–P3 priorities and include a fix plan. Review writes a report; use `improve` to apply changes.

Figma links can provide design context and screenshots when the integration is connected. Requested edits to a Figma file depend on the available tools and file permissions.

## Motion and browser tools

The bundled motion guidance covers CSS, WAAPI, GSAP, Anime.js, Lottie and Three.js, including reduced-motion behavior and performance checks. Short-video workflows use HyperFrames when the requested output is a video.

Local Python utilities handle reference search, HTML previews and contrast checks using the standard library. The Node detector supports dependency-free `--fast` analysis. Optional browser capture uses `@playwright/cli`; video rendering needs HyperFrames and its runtime dependencies. Check installed versions and browser availability before using these workflows.

## Project output

Design artifacts stay in your project:

```text
design/
  design-system.md     # Visual direction and design decisions
  style-guide.md       # Typography, spacing, accessibility and motion
  content-library.md   # Voice, interface copy and state patterns
  tokens.css           # Web design tokens
  preview.html         # Visual preview
  pages/               # Web page specifications
  screens/             # App screen specifications
  references/          # Selected references
  screenshots/         # Images used for review
  reviews/             # Audit reports and fix plans
  .cache/              # Local workflow state
```

Keep the foundation files, tokens, specifications and reports in version control. Suggested `.gitignore` entries:

```gitignore
design/references/downloaded/
design/screenshots/
design/.cache/
```

## Development

Claude Code uses `.claude-plugin/`, native commands in `commands/` and the auditor adapter in `agents/`. Codex uses `.codex-plugin/`, the marketplace in `.agents/plugins/` and the entry skill in `skills/design-builder/`.

Shared knowledge lives in `skills/design/`, with supporting skills for motion, browser capture and Figma. See [host compatibility](references/host-compatibility.md) for resource paths and optional capabilities, and [AGENTS.md](AGENTS.md) for maintenance instructions.

Validate a checkout:

```sh
python3 scripts/validate_plugin.py
python3 -m unittest discover -s skills/design/scripts -p 'test_*.py'
```

## App Builders Club

Design Builder is an open-source tool from [App Builders Club](https://app-builders.club). Explore [MVP Builder](https://github.com/app-builders-club/mvp-builder) for a development workflow built around specifications, tests and self-review.

## Credits

Built on work from [Impeccable](https://github.com/pbakaus/impeccable), [Emil Kowalski Design Skill](https://emilkowal.ski/skill), [Taste Skill](https://github.com/Leonxlnx/taste-skill), [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), and [Design Motion Principles](https://github.com/kylezantos/design-motion-principles). See [NOTICE.md](NOTICE.md) for attribution.

## License

[MIT](LICENSE).
