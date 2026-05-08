# Satellite Configuration Skills

Project skills live in this folder and can be invoked explicitly in prompts.

## How to Use

- Ask the agent to use a skill by name.
- Be specific about the object type and expected scope.
- For new object types, prefer end-to-end skills that update all roles consistently.
- Prefer `redhat.satellite` roles/modules when available; use `ansible.builtin.uri` only when no supported role/module exists.

## Recommended Invocation Pattern

Use prompts like:

- `Use add-object-type-end-to-end to add satellite_compute_resources support.`
- `Use extend-filetree-create-object-type to export satellite_compute_resources.`
- `Use extend-filetree-read-object-type to ingest satellite_compute_resources from .d files.`
- `Use extend-dispatch-object-type to apply satellite_compute_resources in dispatch.`
- `Use promote-content to move RHEL9-Standard to Production.`

## Consistency Expectations

When adding a new object type, update all of these in the same change set:

- `roles/filetree_create`
- `roles/filetree_read`
- `roles/dispatch`

Keep naming and tags aligned:

- data list: `satellite_<resource_plural>`
- export task: `get_<domain>.yaml`
- dispatch task: `satellite_<domain>.yaml`
- export template: `satellite_<resource_plural>.yaml.j2`
- filetree dir: `satellite_<resource_plural>.d/`

## Auto-Applied Rules

Repository conventions are enforced through:

- `.cursor/rules/satellite-general.mdc`

That rule is configured with `alwaysApply: true`.
