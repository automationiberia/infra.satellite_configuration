<!--
# Red Hat Communities of Practice AAP Configuration Extended Collection
-->

# Automation Iberia - Satellite Configuration Collection (automationiberia.satellite_configuration)

![pre-commit tests](https://github.com/automationiberia/satellite_configuration/actions/workflows/pre-commit.yml/badge.svg)
![Release](https://github.com/automationiberia/satellite_configuration/actions/workflows/release.yml/badge.svg)
<!-- Further CI badges go here as above -->

This Ansible Collection provides **Configuration as Code** for **Red Hat Satellite** using Ansible.
It allows to **export** an existing Satellite configuration into a file tree and, later, **import** (apply) that configuration back into Satellite in a repeatable and automated way.

The collection is designed to work both with `ansible-playbook` and with `ansible-navigator` (Execucion Environments).

## Features

- Export Satellite configuration to YAML files
- Import Satellite configuration from YAML files
- Uses official `redhat.satellite` Ansible modules

## Requirements

The only one collection required by `automationiberia.satellite_configuration` is the `redhat.satellite`. You can copy this `requirements.yaml` file example:

```yaml
---
collections:
  - name: automationiberia.satellite_configuration
  - name: redhat.satellite
...
```

### Ansible, Python and other requirements

The following are also requirements:

- Ansible Core >= 2.14
- Red Hat Satellite 6.17
- Access to Satellite API
- One of the following:
  - `ansible-playbook`
  - `ansible-navigator` (recommended)

## Links to Satellite Collections

|                                      Collection Name                                                          |            Purpose                        |
|:-------------------------------------------------------------------------------------------------------------:|:-----------------------------------------:|
| [automationiberia.satellite_configuration repo](https://github.com/automation_iberia/satellite_configuration) | Export/Import Satellite Configuration     |
| [redhat.satellite repo](https://github.com/RedHatSatellite/satellite-ansible-collection.git)                  | Communicate with the Satellite Server API |

## Installing this collection

You can install the `automationiberia.satellite_configuration` collection with the Ansible Galaxy CLI (the dependency -redhat.satellite- will be installed automatically when possible):

```console
ansible-galaxy collection install automationiberia.satellite_configuration
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: automationiberia.satellite_configuration
  - name: redhat.satellite
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
...
```

## Using this collection

Examples of how to run the playbooks in the `playbooks` directory can be found at [`tests/README.md`](tests/README.md).

### Scale at your needs

The input data can be organized in a very flexible way, letting the user use anything from a single file to an entire file tree to store the satellite objects definitions, which could be used as a logical segregation, as needed in real scenarios.

## See Also

- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](https://github.com/automationiberia/satellite_configuration/blob/devel/CHANGELOG.rst).

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `devel` branch.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Satellite Configuration repository](https://github.com/automationiberia/satellite_configuration).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/automationiberia/satellite_configuration/blob/devel/.github/CONTRIBUTING.md)

## Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://github.com/automationiberia/satellite_configuration/blob/devel/LICENSE) to see the full text.
