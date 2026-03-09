# Testing the collection

Following there's an example of how this collection can be used to export and import Satellite Configuration.

## Export your configuration using the following commands

* Using `ansible-playbook`

  ```console
  ansible-playbook automationiberia.satellite_configuration.run_filetree_create.yaml -e@vars/satellite.yaml -e '{output_path: /tmp/satellite_output}'
  ```

* Using `ansible-navigator`

  ```console
  ansible-navigator run automationiberia.satellite_configuration.run_filetree_create.yaml \
    --tags settings \
    --eei registry.redhat.io/ansible-automation-platform-26/ee-supported-rhel9 \
    --pp never \
    -m stdout \
    --eev ~/satellite-configuration:~/satellite-configuration/tests/collections/ansible_collections/automationiberia/satellite_configuration \
    --eev ~/satellite-configuration:~/satellite-configuration \
    -- \
    -e@~/satellite-configuration/tests/vars/satellite.yaml \
    -e '{output_path: ~/satellite-configuration/tests/satellite_output}'
  ```

## Import your configuration as code using the following commands

* Using `ansible-playbook`

  ```console
  ansible-playbook -i localhost, automationiberia.satellite_configuration.run_filetree_read.yaml -e@vars/satellite.yaml
  ```

## Role Input Variables

### Role: `dispatch`

| Variable Name | Default Value | Description |
| --- | --- | --- |
| `satellite_username` | `{{ lookup("env", "SATELLITE_SERVER_URL") }}` | The username to connect to the Satellite instance |
| `satellite_password` | `{{ lookup("env", "SATELLITE_USERNAME") }}` | The password to connect to the Satellite instance |
| `satellite_server_url` | `{{ lookup("env", "SATELLITE_PASSWORD") }}` | The Satellite instance's URL/IP |
| `content_views_purge_count` | `6` | The number of content view versions to maintain into the Satellite instance after publishing new versions |
| `satellite_configuration_dispatch_secure_logging` | `True` | Whether or not to include the sensitive information in the logs. Set this value to true if you will be providing your sensitive values from elsewhere. |

### Role: `filetree_create`

| Variable Name | Default Value | Description |
| --- | --- | --- |
| `output_path` | `/tmp/satellite_filetree_config` | The path to the output directory where all the generated yaml files with the corresponding Objects as code will be written to |

### Role: `filetree_read`

<table>
  <thead>
    <tr>
      <th>Variable Name</th>
      <th>Default Value</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>satellite_configuration_filetree_read_secure_logging</code></td>
      <td><code>true</code></td>
      <td>Whether or not to include the sensitive information in the logs. Set this value to true if you will be providing your sensitive values from elsewhere.</td>
    </tr>
    <tr>
      <td><code>satellite_activation_keys</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Activation Keys.</td>
    </tr>
    <tr>
      <td><code>satellite_auth_sources_ldap</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Authenticator Sources (LDAP)</td>
    </tr>
    <tr>
      <td><code>satellite_content_credentials</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Content Credentials</td>
    </tr>
    <tr>
      <td><code>satellite_content_view_filters</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Content View Filters</td>
    </tr>
    <tr>
      <td><code>satellite_content_views</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Content Views</td>
    </tr>
    <tr>
      <td><code>satellite_domains</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Domains</td>
    </tr>
    <tr>
      <td><code>satellite_host_collections</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Host Collections</td>
    </tr>
    <tr>
      <td><code>satellite_hostgroups</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Host Groups</td>
    </tr>
    <tr>
      <td><code>satellite_lifecycle_environments</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Lifecycle Environments</td>
    </tr>
    <tr>
      <td><code>satellite_locations</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Locations</td>
    </tr>
    <tr>
      <td><code>satellite_operatingsystems</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Operating Systems</td>
    </tr>
    <tr>
      <td><code>satellite_organizations</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Organizations</td>
    </tr>
    <tr>
      <td><code>satellite_partition_tables</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Partition Tables</td>
    </tr>
    <tr>
      <td><code>satellite_products</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Products</td>
    </tr>
    <tr>
      <td><code>satellite_provisioning_templates</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Provisioning Templates</td>
    </tr>
    <tr>
      <td><code>satellite_repositories</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Repositories</td>
    </tr>
    <tr>
      <td><code>satellite_repository_sets</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Repository Sets</td>
    </tr>
    <tr>
      <td><code>satellite_settings</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Settings</td>
    </tr>
    <tr>
      <td><code>satellite_subnets</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Subnets</td>
    </tr>
    <tr>
      <td><code>satellite_sync_plans</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite Synchronization Plans</td>
    </tr>
    <tr>
      <td><code>satellite_usergroups</code></td>
      <td><code>[]</code></td>
      <td>List with the Satellite User Groups</td>
    </tr>
    <tr>
      <td><code>satellite_configuration_filetree_read_tasks</code></td>
      <td><a href="https://github.com/automationiberia/satellite-configuration/blob/a3a7658d78a04fb15466461763c946c0c8c3a455/roles/filetree_read/defaults/main.yml#L29-L50">See defaults file</a></td>
      <td>List to define how to read each object type. Each list item needs the following information:
        <ul>
          <li> <strong>name</strong>: Name of the Object Type,
          <li> <strong>var</strong>: Variable that contains the Objects for that object type,
          <li> <strong>tags</strong>: Tags to filter the tasks to be executed/skipped,
          <li> <strong>path</strong>: Path where the CaC files are found for the current object type
        </ul>
      </td>
    </tr>
  </tbody>
</table>
