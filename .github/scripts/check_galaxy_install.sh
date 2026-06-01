#!/usr/bin/env bash
# Verify the collection can be built and installed locally (CI runs the same with deps).
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

echo "Checking collection build/install with --no-deps..."
ansible-galaxy collection install "${repo_root}" --no-deps -p "${collections_path}"

if [[ -z "${ANSIBLE_GALAXY_SERVER_PUBLISHED_TOKEN:-}" && -z "${ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN:-}" ]]; then
  echo "Skipping dependency resolution check (Automation Hub token not set)."
  echo "CI resolves redhat.satellite:5.8.0 from console.redhat.com using GALAXY_INFRA_KEY."
  exit 0
fi

echo "Checking dependency resolution (redhat.satellite:5.8.0)..."
ansible-galaxy collection install "${repo_root}" -p "${collections_path}" --force

echo "Collection install check passed."
