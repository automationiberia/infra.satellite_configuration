# Ansible Collection - automationiberia.satellite_configuration

This repository provides **Configuration as Code** for **Red Hat Satellite** using Ansible.  
It allows you to **export** an existing Satellite configuration into a file tree and later **import** (apply) that configuration back into Satellite in a repeatable and automated way.

The project is based on the `automationiberia.satellite_configuration` Ansible collection and is designed to work both with `ansible-playbook` and `ansible-navigator` (Execution Environments).

Examples of how to run the playbooks in the `playbooks` directory can be found at [`tests/README.md`](tests/README.md).

---

## Features

- Export Satellite configuration to YAML files
- Import Satellite configuration from YAML files
- Uses official `redhat.satellite` Ansible modules

---

## Requirements

- Ansible Core >= 2.14
- Red Hat Satellite 6.17
- Access to Satellite API
- One of the following:
  - `ansible-playbook`
  - `ansible-navigator` (recommended)

### Required Ansible Collections

```bash
ansible-galaxy collection install automationiberia.satellite_configuration
ansible-galaxy collection install redhat.satellite
```
