# Satellite Configuration Extract Script

This is an Ansible script for the extraction of configuration information from the existing Satellite deployment.
Verified and tested on the Sattelite version 6.11.

1. Configure variables in the vars/test_vars.yml file.

2. Use the following command to run the script:
`ansible-playbook extract_satellite_config.yml`

3. Review extracted configuration in the configs/ folder.
