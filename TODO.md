# TODO — checks

Mark `- [x]` when the criterion is satisfied. Last audit: 2026-05-05.

## RBAC

- [ ] Custom Satellite roles are exported in `filetree_create`.
- [ ] `satellite_roles` (or equivalent) is declared and loaded in `filetree_read/defaults/main.yml`.
- [ ] Dispatch applies custom roles via `redhat.satellite` (wired in `dispatch/tasks/main.yaml` with a tag).
- [ ] Local Satellite users are exported, readable, and dispatched (full loop).
- [ ] Role organization/location (and other) filters are represented in YAML and applied by dispatch.
- [ ] README states clearly what RBAC is in scope vs out of scope.

## Dispatch parity (export → import)

- [ ] Domains: `include_tasks` + `domains` tag in `dispatch/tasks/main.yaml`.
- [ ] Subnets: `include_tasks` + `subnets` tag in `dispatch/tasks/main.yaml`.
- [ ] Host groups: `include_tasks` + `hostgroups` tag in `dispatch/tasks/main.yaml`.
- [ ] `filetree_read` README tag list matches dispatch tags for domains, subnets, hostgroups.

## Content views

- [ ] Content view filters: either enabled in dispatch with a defined tag and order, or removed with docs updated.
- [x] CV publish/promote: enabled via `satellite_configuration_dispatch_content_view_publish_promote`; auto-derived from `satellite_content_views` or explicit `satellite_content_view_versions`.
- [ ] Composite content views: implemented end-to-end, or stub config removed and docs updated.

## Tests

- [ ] `tests/satellite_output/satellite_content_view_filters.yaml` exists if filters stay supported.
- [ ] Read → dispatch test path covers domains, subnets, and hostgroups once dispatch exists.

## Hygiene

- [ ] Lifecycle YAML `permissions` keys: confirmed harmless or stripped in templates/dispatch.
- [ ] New surface area ships with `changelogs/fragments/` and version bump per release rules.

## Cursor skills (Satellite MCP)

- [ ] Satellite MCP server is configured and tool descriptors are known (server id, tool names, auth if any).
- [ ] One or more **Cursor Agent Skills** (`SKILL.md` + optional `reference.md`) teach the agent when to use Satellite MCP vs Ansible/collection workflows.
- [ ] Each skill documents **read tool schema first**, then `call_mcp_tool` with correct arguments (match MCP descriptor JSON).
- [ ] Skills live in **project** `.cursor/skills/<skill-name>/` (repo-shared) or **personal** `~/.cursor/skills/` — choice documented in skill or README.
- [ ] Skill `description` frontmatter includes trigger terms (Satellite, MCP, content views, hosts, etc.) so invocation matches intent.
- [ ] Do **not** place custom skills under `~/.cursor/skills-cursor/` (reserved for Cursor-built-in skills).
