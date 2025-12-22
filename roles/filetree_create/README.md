# Satellite Configuration filetree_create role

This is an Ansible script for the exportation of configuration information from the existing Satellite deployment.
Verified and tested on the Sattelite version 6.11.

1. Configure variables in the vars/test_vars.yaml file.

2. Use the following command to run the script:
`ansible-playbook filetree_create.yaml`

3. Review generated configuration in the configs/ folder.
