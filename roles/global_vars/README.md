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

## License

GPLv3+
