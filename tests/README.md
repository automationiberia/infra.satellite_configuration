# Export your configuration using the following commands:

* Using `ansible-playbook`
  ```console
  $ ansible-playbook automationiberia.satellite_configuration.run_filetree_create.yaml -e@vars/satellite.yaml -e '{output_path: /tmp/satellite_output}'
  ```
* Using `ansible-navigator`
  ```console
  $ ansible-navigator run automationiberia.satellite_configuration.run_filetree_create.yaml \
      --tags settings \
      --eei registry.redhat.io/ansible-automation-platform-26/ee-supported-rhel9 \
      --pp never \
      -m stdout \
      --eev /home/pgoku/satellite-configuration:/home/pgoku/satellite-configuration/tests/collections/ansible_collections/automationiberia/satellite_configuration \
      --eev /home/pgoku/satellite-configuration:/home/pgoku/satellite-configuration \
      -- \
      -e@/home/pgoku/satellite-configuration/tests/vars/satellite.yaml \
      -e '{output_path: /home/pgoku/satellite-configuration/tests/satellite_output}'
  ```

# Import your configuration as code using the following commands:

* Using `ansible-playbook`
  ```console
  ansible-playbook -i localhost, automationiberia.satellite_configuration.run_filetree_read.yaml -e@vars/satellite.yaml
  ```

