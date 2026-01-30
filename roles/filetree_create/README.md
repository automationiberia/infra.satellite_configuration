# automationiberia.satellite.filetree_create

The role `automationiberia.satellite.filetree_create` is intended to be used as the first step to begin using the Configuration as Code on Red Hat Satellite, when you already have a running instance of any of them. Obviously, you also could start to write your objects as code from scratch, but the idea behind the creation of that role is to simplify your lives and make that task a little bit easier.

## Requirements

* Collections:
  * [redhat.satellite][link_redhat.satellite]: Can be installed with the command `ansible-galaxy collection install redhat.satellite` (Requires [configuration][link_galaxy_configuration]).

* Binaries:
  * [`yq`][link_yq]: Can be installed with the command `dnf install yq`.

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

## Example Playbook

```yaml
---
- name: Export Satellite Configuration
  hosts: localhost
  connection: local
  gather_facts: false
  module_defaults:
    redhat.satellite.organization_info: &satellite_creds
      username: "{{ satellite.admin.username }}"
      password: "{{ satellite.admin.password }}"
      server_url: "{{ satellite.server_url }}"
      validate_certs: "{{ satellite.validate_certs }}"
  tasks:
    - name: Ensure that the output_path exists
      ansible.builtin.file:
        path: "{{ output_path }}"
        owner: "{{ satellite.template.owner }}"
        group: "{{ satellite.template.group }}"
        mode: "0777"
        state: directory
      tags: always

    - name: Get Organizations
      import_role:
        name: automationiberia.satellite_configuration.filetree_create

    - name: "Block to fix the output files' format"
      tags: always
      block:
        - name: "Search for all the generated files"
          ansible.builtin.find:
            paths: "{{ output_path }}"
            recurse: true
            patterns:
              - '*.yaml'
              - '*.yml'
          register: _generated_files

        - name: "Re-write all the generated files to make them more readable (Content Credentials special case)"
          ansible.builtin.shell: |
            yq -i '(.satellite_content_credentials[].content) |= (trim + "\n") | (.satellite_content_credentials[].content) style="literal"' '{{ _current_file.path }}'; yq -i -P '{{ _current_file.path }}'
          when: "'content_credentials' in _current_file.path"
          changed_when: true
          loop: "{{ _generated_files.files }}"
          loop_control:
            loop_var: _current_file
            label: "{{ _current_file.path }}"
          # noqa: risky-shell-pipe
          # ^ The shell command above does't use any pipe (only in the yq search)

        - name: "Re-write all the generated files to make them more readable"
          ansible.builtin.shell: "/usr/bin/env yq -i -P '{{ _current_file.path }}' && echo '...' >> '{{ _current_file.path }}'"
          changed_when: true
          loop: "{{ _generated_files.files }}"
          loop_control:
            loop_var: _current_file
            label: "{{ _current_file.path }}"
...
```

The output files are all located in the same directory. Each file contains a YAML list with all the objects belonging to the same object type. This output format allows to load all the objects both from the standard Ansible `group_vars` and from the `automationiberia.satellite_configuration.filetree_read` role.

The exportation can be triggered with the following command:

```console
ansible-playbook automationiberia.satellite_configuration.run_filetree_create.yaml -e@vars/satellite.yaml -e '{output_path: /tmp/satellite_output}'
```

Where the `vars/satellite.yaml` file is defined as follows:

```yaml
---
satellite:
  server_url: "https://satellite.server.domain.com"
  validate_certs: true
  admin:
    username: username
    password: password
  template:
    owner: '1000'
    group: '1000'
    mode: '0666'
...
```

One example of the generated files follows:

```console
/tmp/satellite_filetree_config
├── satellite_activation_keys.yaml
├── satellite_auth_sources_ldap.yaml
├── satellite_content_credentials.yaml
├── satellite_content_views.yaml
├── satellite_domains.yaml
├── satellite_host_collections.yaml
├── satellite_hostgroups.yaml
├── satellite_lifecycle_environments.yaml
├── satellite_locations.yaml
├── satellite_operatingsystems.yaml
├── satellite_organizations.yaml
├── satellite_products.yaml
├── satellite_repositories.yaml
├── satellite_repository_sets.yaml
├── satellite_settings.yaml
├── satellite_subnets.yaml
├── satellite_sync_plans.yaml
└── satellite_usergroups.yaml
```

## License

GPLv3+

## Author Information

* [Silvio Pérez][link_silvinux]
* [Ivan Aragonés][link_ivarmu]

[link_yq]: https://mikefarah.gitbook.io/yq/
[link_redhat.satellite]: https://console.redhat.com/ansible/automation-hub/repo/published/redhat/satellite/
[link_galaxy_configuration]: https://console.redhat.com/ansible/automation-hub/repo/published/redhat/satellite/distributions/
[link_silvinux]: https://github.com/silvinux
[link_ivarmu]: https://github.com/ivarmu
