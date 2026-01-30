# automationiberia.satellite_configuration.dispatch

## Description

An Ansible Role to import existing configuration as code to a Red Hat Satellite server. This configuration can be loaded both using Ansible inventory variables or the role `automationiberia.satellite_configuration.filetree_read`.

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
| `output_path` | `/tmp/satellite_filetree_config` | no | str | The path to the output directory where all the generated `yaml` files with the corresponding objects as code will be written to. |
| `satellite_<object_type_variable>` | N/A | yes | list | The input configuration to be applied. Each object type is defined in a dedicated variable. The list of valid input variables can be found at the [`automationiberia.satellite_configuration.filetree_read` defaults' file][link_filetree_read_defaults] |

## Example Playbook

```yaml
---
- name: Playbook to test the roles 'automationiberia.satellite_configuration'.'filetree_read' and 'dispatch'
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
    - role: automationiberia.satellite_configuration.filetree_read
    - role: automationiberia.satellite_configuration.dispatch
...
```

```console
ansible-playbook -i localhost, automationiberia.satellite_configuration.run_filetree_read.yaml -e@vars/satellite.yaml
```

## License

[GPLv3+](https://github.com/redhat-cop/infra.aap_configuration/blob/devel/LICENSE)

[link_filetree_read_defaults]: https://github.com/automationiberia/satellite-configuration/blob/b458b309405ba9aa61b0f7de4078c01169c48419/roles/filetree_read/defaults/main.yml#L6-L47
