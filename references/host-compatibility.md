# Host compatibility

These rules apply to all Design Builder workflows and clarify legacy examples.
Follow the host's higher-priority instructions and the user's current scope.

## Entry points and paths

Claude Code loads `.claude-plugin/plugin.json`, commands and the native auditor
agent. Codex loads `.codex-plugin/plugin.json` and the `design-builder` skill;
command files remain shared workflow recipes, not native Codex slash commands.
Translate suggested `/design-builder:<action>` next steps into `$design-builder
<action>` in Codex. Claude-only frontmatter is not a tool permission grant in Codex.

Resolve `skills/`, `commands/`, `agents/`, and `references/` paths in these recipes
against the installed **plugin root**, never the target project's working directory.
Relative Markdown links resolve against the file containing them. Determine the
root from the loaded skill/command's absolute location; do not assume that
`CLAUDE_PLUGIN_ROOT` is exported into ordinary shell calls. Before shell examples,
set `DESIGN_BUILDER_ROOT` to that observed absolute root using proper shell quoting.
Use `python3 "$DESIGN_BUILDER_ROOT/skills/design/scripts/search.py" ...` or
`node "$DESIGN_BUILDER_ROOT/skills/design/scripts/detect-antipatterns.mjs" --fast ...`.
Write `design/`, `.impeccable.md`, source patches and reports in the **user project**.
Never write generated project artifacts into the installed plugin cache.

## Tools and optional capabilities

Discover available tool names and schemas before calling. `mcp__designlib__*`,
`mcp__plugin_figma_figma__*`, `Read`, `Edit`, `Bash`, and `Task` in older examples
are logical roles, not portable literal names. Use the host's actual file, shell,
browser and MCP tools. `get_design_reference(type, filters)` is resolver
pseudocode, not an implemented tool or Python function.

DesignLib and Figma are optional. Use project tokens first, then available
DesignLib, local CSV and platform references. On an unavailable server or auth
failure, mention the limitation once and continue with those sources. Never
invent catalog IDs, fetched records, screenshots or a successful connection.
Landing patterns, whole-page references and animation recipes are remote catalog
features, not local CSV databases. Label any freely generated fallback honestly.
The MCP endpoints are in `.mcp.json`; native plugin installation registers them.
Avoid adding duplicate global MCP servers just to compensate for an inactive plugin.

For `/review`, run the shared audit in `skills/design/references/audit-workflow.md`.
Delegate to Claude's `design-auditor` only when supported and allowed by the host;
otherwise execute the same workflow inline with the same report contract.
Prefer an existing browser integration when it supplies the necessary capture.
If using Playwright CLI, load its skill and use the scoped `@playwright/cli` package.
A failed or absent browser means code-only review, not invented visual conclusions.

## Context and authority

Reuse supplied briefs and accepted choices. Setup discovery and visual candidates
are useful when a new direction is undecided; do not re-interview for a scoped fix,
review, an existing system, or a sufficiently specified/delegated implementation.
Make requested edits within scope without redundant confirmation. Reviews write
reports but do not edit implementation. Figma writes require a user request that
covers editing that file; a URL supplied for inspection alone is not such a request.
Do not create native agents or external resources simply because a recipe names one.

## Freshness

Live schemas and installed dependency versions take precedence over reference
examples. Check current primary documentation for version-sensitive APIs before
implementation; preserve existing project versions unless an upgrade is requested.
Catalog counts, plan limits and seat eligibility change; discover them live rather
than treating a bundled count or quota as a guarantee. UI style heuristics are
preferences, not accessibility failures; respect intentional project branding.
