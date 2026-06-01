#!/usr/bin/env bash
# Verify the collection under development installs from the local tree (no remote lookup).
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tmp_dir="$(mktemp -d)"
ansible_local_tmp="${tmp_dir}/ansible-local"
collections_path="${tmp_dir}/collections"

cleanup() {
  rm -rf "${tmp_dir}"
}
trap cleanup EXIT

mkdir -p "${ansible_local_tmp}" "${collections_path}"

export ANSIBLE_LOCAL_TEMP="${ansible_local_tmp}"
export ANSIBLE_COLLECTIONS_PATH="${collections_path}"

echo "Checking collection install from repository with --no-deps..."
ansible-galaxy collection install "${repo_root}" --no-deps -p "${collections_path}"

installed="${collections_path}/ansible_collections/infra/satellite_configuration"
if [[ ! -d "${installed}" ]]; then
  echo "ERROR: expected collection at ${installed}" >&2
  exit 1
fi

echo "Collection install check passed."
