# infra.satellite_configuration.global_vars

## Description

Role that defines static variables shared across other roles in this collection. Consumer roles declare a dependency in `meta/main.yml`:

```yaml
dependencies:
  - role: global_vars
```

## Provided variables

| Variable Name | Default | Description |
| :--- | :---: | :--- |
| `satellite_builtin_role_name_skips` | see `defaults/main.yml` | Built-in / locked Foreman role names skipped on export and import |
| `satellite_builtin_role_name_skips_extra` | `[]` | Additional role names to skip on export and import |
| `satellite_configuration_sensitive_vars` | see `defaults/main.yml` | CaC list names that may contain secrets; used by `read_contents.yml` to scope `no_log` per object type in the ingest loop |
| `satellite_redhat_repository_url_substring` | `cdn.redhat.com` | URL substring used to exclude Red Hat CDN repositories from custom repository export/dispatch |
| `satellite_configuration_filetree_read_raw_template_vars` | see `defaults/main.yml` | CaC list names loaded via `slurp` + `from_yaml` in `filetree_read` (no Jinja templating on fragment contents) |
| `satellite_configuration_filetree_path` | `/tmp/satellite_filetree_config` | Base directory for export and import `.d/` fragments |
| `satellite_configuration_vault_placeholder` | `CHANGEME` | Scalar placeholder written into generated `vault_template.yaml` |
| `satellite_configuration_vault_template_vars` | see `defaults/main.yml` | Vault variable names generated in `vault_template.yaml` and referenced from CaC fragments |
| `satellite_settings_host_specific_names` | see `defaults/main.yml` | Host-specific setting names exported with `vault_satellite_settings_host_specific` refs |

## License

GPLv3+
