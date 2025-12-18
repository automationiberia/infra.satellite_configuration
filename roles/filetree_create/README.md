# Satellite Configuration filetree_create role

This is an Ansible script for the exportation of configuration information from the existing Satellite deployment.
Verified and tested on the Sattelite version 6.11.

1. Configure variables in the vars/test_vars.yml file.

2. Use the following command to run the script:
`ansible-playbook filetree_create.yml`

3. Review generated configuration in the configs/ folder.
