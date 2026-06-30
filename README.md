<!--
# Red Hat Communities of Practice AAP Configuration Extended Collection
-->

# Automation Iberia - Satellite Configuration Collection (infra.satellite_configuration)

![pre-commit tests](https://github.com/redhat-cop/infra.satellite_configuration/actions/workflows/pre-commit.yml/badge.svg)
![Release](https://github.com/redhat-cop/infra.satellite_configuration/actions/workflows/release.yml/badge.svg)
<!-- Further CI badges go here as above -->

This Ansible Collection provides **Configuration as Code** for **Red Hat Satellite** using Ansible.
It allows to **export** an existing Satellite configuration into a file tree and, later, **import** (apply) that configuration back into Satellite in a repeatable and automated way.

The collection is designed to work both with `ansible-playbook` and with `ansible-navigator` (Execucion Environments).

## Features

- Export Satellite configuration to YAML files
- Import Satellite configuration from YAML files
- Uses official `redhat.satellite` Ansible modules

## Requirements

The only one collection required by `infra.satellite_configuration` is the `redhat.satellite`. You can copy this `requirements.yaml` file example:

```yaml
---
collections:
  - name: infra.satellite_configuration
  - name: redhat.satellite
...
```

### Ansible, Python and other requirements

The following are also requirements:

- Ansible Core >= 2.16
- Python library `PyYAML` (used by the YAML formatter module)
- Python library `jmespath` (required by Ansible's `json_query` filter in export tasks)
- Red Hat Satellite 6.17
- Access to Satellite API
- One of the following:
  - `ansible-playbook`
  - `ansible-navigator` (recommended)

## Links to Satellite Collections

|                                      Collection Name                                                          |            Purpose                        |
|:-------------------------------------------------------------------------------------------------------------:|:-----------------------------------------:|
| [infra.satellite_configuration repo](https://github.com/redhat-cop/infra.satellite_configuration)             | Export/Import Satellite Configuration     |
| [redhat.satellite repo](https://github.com/RedHatSatellite/satellite-ansible-collection.git)                  | Communicate with the Satellite Server API |

## Installing this collection

You can install the `infra.satellite_configuration` collection with the Ansible Galaxy CLI (the dependency -redhat.satellite- will be installed automatically when possible):

```console
ansible-galaxy collection install infra.satellite_configuration
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.satellite_configuration
  - name: redhat.satellite
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
...
```

## Using this collection

Examples of how to run the playbooks in the `playbooks` directory can be found in the [`tests/README`](https://github.com/redhat-cop/infra.satellite_configuration/blob/devel/tests/README.md).

### Configuration file layout

Export and import share the same layout under `satellite_configuration_filetree_path` (default `/tmp/satellite_filetree_config`):

```text
satellite_configuration_filetree_path/
├── satellite_organizations.d/
│   └── satellite_organizations.yaml
├── satellite_settings.d/
│   └── satellite_settings.yaml
├── vault_template.yaml
└── …
```

Each object type uses a `satellite_<resource_plural>.d/` directory with one or more YAML fragments. There is no organization or environment path nesting — export output from `filetree_create` can be consumed directly by `filetree_read`.

`filetree_create` also writes `vault_template.yaml` at the tree root. CaC fragments reference its `vault_*` variables for LDAP bind passwords, Internal-user passwords, encrypted settings, host-specific settings, and installation-medium target FQDN. Replace placeholder values, optionally encrypt the file, and pass it on import with `-e@…/vault_template.yaml`.

The [`configs/`](configs/) directory in this repository is an example **greenfield** tree: hand-authored desired state using the same `.d/` layout, without exporting from an existing Satellite.

### Subscription manifest

Content operations require a subscription manifest on the target organization. Before repository and product tasks, `dispatch` validates that a manifest is present (`satellite_configuration_dispatch_manifest_validate: true` by default). Upload a manifest with:

```yaml
satellite_configuration_dispatch_manifest_upload: true
satellite_manifest_path: /path/to/manifest.zip
satellite_configuration_dispatch_manifest_organization: "Default Organization"
```

Set `satellite_configuration_dispatch_manifest_validate: false` only when content tags are skipped.

### Supported object types

The three roles (`filetree_create`, `filetree_read`, `dispatch`) cover the object types listed in [`filetree_read` defaults](roles/filetree_read/defaults/main.yml).

The following Satellite objects are **not yet** covered end-to-end (Issue #11); extend the collection using the skills under `.cursor/skills/` when needed:

- Compute resources and compute profiles
- Global parameters
- SCAP content and policies
- Job templates
- Webhooks
- HTTP proxies
- Remote execution features

### Scale at your needs

The input data can be organized in a very flexible way, letting the user use anything from a single file to an entire file tree to store the satellite objects definitions, which could be used as a logical segregation, as needed in real scenarios.

## See Also

- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](https://github.com/redhat-cop/infra.satellite_configuration/blob/devel/CHANGELOG.rst).

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `devel` branch.

## Support

As Red Hat Ansible Validated Content, this collection is entitled to support through the Ansible Automation Platform (AAP) using the **Create issue** button on the top right corner of the collection page in Red Hat Ansible Automation Hub.

If a support case cannot be opened with Red Hat and the collection has been obtained either from Galaxy or GitHub, community help may be available on the [Ansible Forum](https://forum.ansible.com/).

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Satellite Configuration repository](https://github.com/redhat-cop/infra.satellite_configuration).
More information about contributing can be found in our [Contribution Guidelines](https://github.com/redhat-cop/infra.satellite_configuration/blob/devel/.github/CONTRIBUTING.md).

## Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://github.com/redhat-cop/infra.satellite_configuration/blob/devel/LICENSE) to see the full text.
