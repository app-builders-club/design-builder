---
name: design-builder
description: Design systems, web pages, iOS screens, UI implementation, improvements and design reviews. Use when the user asks Design Builder to setup, design_page, design_screen, build, improve or review a product interface, or needs design-led UI work with local references, motion, browser capture or Figma.
---

# Design Builder

Read [host compatibility](../../references/host-compatibility.md) first, then the
[design knowledge base](../design/SKILL.md). Determine the plugin root from this
file's absolute path: it is two directories above this skill directory.

Route the user's intent to ONE shared workflow below and execute it. These are
Markdown instructions to read, not shell commands or tools to invent.

| Intent | Workflow |
|---|---|
| setup, start, new design foundation | [setup](../../commands/setup.md) |
| design_page, plan a web page | [design_page](../../commands/design_page.md) |
| design_screen, plan an app screen | [design_screen](../../commands/design_screen.md) |
| build, implement approved specifications | [build](../../commands/build.md) |
| improve, fix or refine existing UI | [improve](../../commands/improve.md) |
| review, audit without source edits | [review](../../commands/review.md) |

In Codex use `$design-builder review src/`, `$design-builder setup`, or ordinary
language. Claude Code also keeps `/design-builder:review`, `:setup`, `:start`,
`:design_page`, `:design_screen`, `:build`, and `:improve`.
For standalone animation, video or Figma operations, load the relevant sister
skill linked from the knowledge base rather than forcing a setup interview.

Reuse the brief, existing design system and decisions already made in this chat.
Ask only for missing choices that materially affect the requested work. A bounded
review/fix needs no brand interview. If the user delegates design choices, make
and state reasonable choices and continue through the authorized implementation.
