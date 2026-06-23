# infra.satellite_configuration.dispatch

## Description

An Ansible Role to import existing configuration as code to a Red Hat Satellite server. This configuration can be loaded both using Ansible inventory variables or the role `infra.satellite_configuration.filetree_read`.

## Role Variables

The following variables are required for that role to work properly:

| Variable Name | Default Value | Required | Type | Description |
| :------------ | :-----------: | :------: | :------: | :---------- |
| `satellite` | N/A | yes | dict | Contains all the information needed to connect to the Red Hat Satellite instance. Fields are described below. |
| `satellite.server_url` | N/A | yes | str | Red Hat Satellite Server URL (must include the protocol  to be used 'https://'). |
| `satellite.validate_certs` | N/A | yes | str | Specifies whether to validate certificates or not when connecting to Red Hat Satellite server. |
| `satellite.admin` | N/A | yes | dict | Contains all the information related to the user to use to connect to the Red Hat Satellite server. Fields are described below. |
| `satellite.admin.username` | N/A | yes | str | Specifies the username to be used. |
| `satellite.admin.password` | N/A | yes | str | Specifies the password to be used. |
| `satellite.template` | N/A | yes | dict | Contains the information needed for the generated files' permissions. Fields are described below. |
| `satellite.template.owner` | N/A | yes | str | Specifies the user name/UID who the generated files will belong to. |
| `satellite.template.group` | N/A | yes | str | Specifies the group name/GID who the generated files will belong to. |
| `satellite.template.mode` | N/A | yes | str | Specifies the permissions the generated files will have. |
| `output_path` | see `satellite_configuration_filetree_path` in role `global_vars` | no | str | Alias used by `filetree_create`; same base path as import. |
| `satellite_configuration_filetree_path` | `/tmp/satellite_filetree_config` | no | str | Base directory for `satellite_<type>.d/` CaC fragments (export and import). |
| `satellite_configuration_dispatch_manifest_upload` | `false` | no | bool | When `true`, uploads `satellite_manifest_path` via `redhat.satellite.manifest` before content tasks. |
| `satellite_configuration_dispatch_manifest_validate` | `true` | no | bool | When `true`, fails early if the target organization has no subscription manifest. |
| `satellite_configuration_dispatch_manifest_organization` | first `satellite_organizations` name or `Default Organization` | no | str | Organization for manifest upload and validation. |
| `satellite_manifest_path` | `""` | when upload enabled | str | Path to manifest zip on the control node. |
| `satellite_manifest_download` | `false` | no | bool | Download manifest from Red Hat Customer Portal before upload (requires RHSM credentials). |
| `satellite_<object_type_variable>` | N/A | yes | list | The input configuration to be applied. Each object type is defined in a dedicated variable. The list of valid input variables can be found at the [`infra.satellite_configuration.filetree_read` defaults' file][link_filetree_read_defaults] |
| `satellite_users_default_password` | unset | no | str | Optional fallback for `redhat.satellite.user` **`user_password`** when a `satellite_users` item omits it. Foreman requires a password to **create** Internal-auth users; prefer **`user_password`** per user from Vault. |
| `dispatch_roles_name_skips_extra` | `[]` | no | list | Additional role names skipped on import (appended to `satellite_builtin_role_name_skips` from role `global_vars`). |
| `satellite_configuration_dispatch_secure_logging` | `true` | no | bool | When `true`, sets `no_log` on dispatch tasks for sensitive object types (users, settings, content credentials, LDAP). Set `false` when debugging. |
| `satellite_configuration_dispatch_content_view_publish_promote` | `true` | no | bool | When `true`, publishes and promotes content views after `content_views` dispatch (tag `cv_publish_promote`). Set `false` to skip or on re-runs when versions already exist. |
| `satellite_content_view_versions` | `[]` | no | list | Optional explicit publish/promote actions for `redhat.satellite.content_view_version`. When empty, actions are derived from `satellite_content_views` export metadata (`versions`, `needs_publish`, `latest_version_environments`). |
| `satellite_configuration_dispatch_host_collection_membership` | `false` | no | bool | When `true`, assigns exported `hosts` to host collections. Default `false` for greenfield imports where hosts do not exist yet. |
| `content_views_purge_count` | `6` | no | int | Keep this many newest versions per content view after publish; passed to `redhat.satellite.content_view_version_cleanup`. |

### `satellite_users` and passwords

Exports do not include passwords. When **creating** a user with **`auth_source: Internal`** (or default Internal), set **`user_password`** on that list entry (from Vault), or define **`satellite_users_default_password`** for bootstrap environments only. Omit `user_password` on existing users you only update.

### `satellite_roles` and built-in roles

Dispatch skips built-in and locked roles from `satellite_roles` (by name via `satellite_builtin_role_name_skips` from role **`global_vars`**, and by `builtin` / `locked` when present in legacy CaC). Append site-specific names with **`dispatch_roles_name_skips_extra`**.

### RBAC and dispatch order

Dispatch applies RBAC objects in dependency order: `auth_sources_ldap` → `organizations` → `locations` → `roles` → `users` → `usergroups`.

Content and provisioning objects run in dependency order after lifecycle environments and optional manifest upload/validation:

`content_credentials` → `products` (initial, without sync plan) → `repository_sets` → `repositories` → `sync_plans` → `products` (sync plan association) → `content_views` → `content_view_filters` → `cv_publish_promote` → `activation_keys` → `host_collections` → `partition_tables` → `provisioning_templates` → `operatingsystems` → `installation_mediums` → `hostgroups`.

User groups only receive direct `users` memberships for logins defined in `satellite_users`; LDAP users are mapped through `external_usergroups`.

## Example Playbook

```yaml
---
- name: Playbook to test the roles 'infra.satellite_configuration'.'filetree_read' and 'dispatch'
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    username: &username "{{ satellite.admin.username }}"
    password: &password "{{ satellite.admin.password }}"
    server_url: &server_url "{{ satellite.server_url }}"
    validate_certs: &validate_certs "{{ satellite.validate_certs }}"
  module_defaults:
    group/redhat.satellite.satellite: &creds
      username: *username
      password: *password
      server_url: *server_url
      validate_certs: *validate_certs
  roles:
    - role: infra.satellite_configuration.filetree_read
    - role: infra.satellite_configuration.dispatch
...
```

```console
ansible-playbook -i localhost, infra.satellite_configuration.run_filetree_read.yaml -e@vars/satellite.yaml
```

## License

[GPLv3+](https://github.com/redhat-cop/infra.satellite_configuration/blob/devel/LICENSE)

[link_filetree_read_defaults]: https://github.com/redhat-cop/infra.satellite_configuration/blob/devel/roles/filetree_read/defaults/main.yml#L6-L53
