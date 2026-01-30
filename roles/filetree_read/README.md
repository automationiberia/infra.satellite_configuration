# automationiberia.satellite_configuration.filetree_read

An ansible role which reads variables from a hierarchical and scalable directory structure which is grouped based on the configuration code life-cycle. It could be used to run the role `automationiberia.satellite_configuration.filetree_read` to load variables followed by `automationiberia.satellite_configuration.dispatch` role to apply the configuration.

## Requirements

This role have no requirements.

## Role Variables

The following Variables set the organization where should be applied the configuration, the absolute or relative of the directory structure where the variables will be stored and the life-cycle environment to use.

|Variable Name|Type|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|:---:|
|`satellite_configuration_filetree_read_tasks`|List(Dict)|See the [defaults file][link_defaults_line_27]|yes|This variable defines all the object types to be read, with the information shown in the `items` Dict below.|
|`items.name`|String|See the [defaults file][link_defaults_line_27]|yes|Name of the object type to be read|
|`items.var`|String|See the [defaults file][link_defaults_line_27]|yes|Name of the variable where to store the objects in memory|
|`items.tags`|String|See the [defaults file][link_defaults_line_27]|yes|Tags to let the playbook filter what object types must be exported|
|`items.path`|String|See the [defaults file][link_defaults_line_27]|yes|Path where are stored the objects to be read for the current object type|

### Input Data Structure

Variables should be stored in yaml files. It could be used vault to encrypt sensitive data when needed.

There's a complete example of the generated files at the [tests/satellite_output][link_satellite_output] directory. Follows a sample for the `satellite_locations`:

```yaml
---
satellite_locations:
  - name: Barcelona
    organizations:
      - red_ribbon
      - red_ribbon_new
      - red_ribbon_new_demo
      - red_ribbon_new_demo_2
      - Umbrella
  - name: Onda
    organizations:
      - red_ribbon
      - Umbrella
...
```

## Role Tags

The role is designed to be used with tags, each tags correspond to an AWX or Automation Controller object to be managed by ansible.

```console
$ ansible-playbook automationiberia.satellite_configuration.run_filetree_create.yaml --list-tags

  play #1 (localhost): Export Satellite Configuration TAGS: []
    TASK TAGS: [activation_keys, always, auth_sources_ldap, content_credentials, content_views, domains, host_collections, hostgroups, lifecycle_environments, locations, operatingsystems, organizations, products, repositories, repository_sets, settings, subnets, sync_plans, usergroups]
```

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

GPLv3+

## Author Information

- [Silvio Pérez][link_silvinux]
- [Ivan Aragonés][link_ivarmu]

[link_satellite_output]: https://github.com/automationiberia/satellite-configuration/tree/devel/tests/satellite_output
[link_defaults_line_27]: https://github.com/automationiberia/satellite-configuration/blob/b458b309405ba9aa61b0f7de4078c01169c48419/roles/filetree_read/defaults/main.yml#L27
[link_silvinux]: https://github.com/silvinux
[link_ivarmu]: https://github.com/ivarmu
