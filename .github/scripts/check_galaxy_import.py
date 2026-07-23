"""Run galaxy-importer the same way CI build-import does, and fail on actionable errors.

Galaxy Importer often logs ansible-doc / lint problems as ERROR/WARNING while still
returning success. CRC review surfaces those lines; this check fails the commit when
they appear so a release is not published with known importer findings.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
IMPORTER_RESULT = REPO_ROOT / "importer_result.json"

# Fail the hook when importer logs these (CRC / Automation Hub review noise that
# slipped through a green import). Match galaxy-importer CustomFormatter + raw
# DocStringLoader messages.
_FAIL_PATTERNS = (
    re.compile(r"^ERROR:", re.MULTILINE),
    re.compile(r"Error running ansible-doc:", re.MULTILINE),
    re.compile(r"The import failed for the following reason:", re.MULTILINE),
    re.compile(r"Unexpected error occurred:", re.MULTILINE),
    re.compile(r"Invalid file paths detected", re.MULTILINE),
    re.compile(r"No collection readme found", re.MULTILINE),
)


def _write_importer_cfg(path: Path) -> None:
    # Match ansible/ansible-content-actions build_import.yaml
    path.write_text("[galaxy-importer]\nCHECK_REQUIRED_TAGS=True\n", encoding="utf-8")


def main() -> int:
    if shutil.which("ansible-doc") is None:
        print("ERROR: ansible-doc not found (install ansible-core).", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory(prefix="galaxy-import-") as tmp_dir:
        cfg_path = Path(tmp_dir) / "galaxy-importer.cfg"
        output_path = Path(tmp_dir) / "artifacts"
        output_path.mkdir(parents=True, exist_ok=True)
        _write_importer_cfg(cfg_path)

        env = os.environ.copy()
        env["GALAXY_IMPORTER_CONFIG"] = str(cfg_path)
        env["ANSIBLE_LOCAL_TEMP"] = str(Path(tmp_dir) / "ansible-local")
        Path(env["ANSIBLE_LOCAL_TEMP"]).mkdir(parents=True, exist_ok=True)

        # galaxy_importer.main writes importer_result.json into CWD; run from tmp.
        cmd = [
            sys.executable,
            "-m",
            "galaxy_importer.main",
            "--git-clone-path",
            str(REPO_ROOT),
            "--output-path",
            str(output_path),
        ]
        print("Running:", " ".join(cmd))
        result = subprocess.run(
            cmd,
            cwd=tmp_dir,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    combined = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    if combined.strip():
        sys.stdout.write(combined)
        if not combined.endswith("\n"):
            sys.stdout.write("\n")

    # Drop accidental CWD artifact if importer was ever run from the repo root.
    if IMPORTER_RESULT.is_file():
        IMPORTER_RESULT.unlink()

    failures = []
    if result.returncode != 0:
        failures.append(f"galaxy-importer exited with code {result.returncode}")

    for pattern in _FAIL_PATTERNS:
        if pattern.search(combined):
            failures.append(f"matched importer failure pattern: {pattern.pattern}")

    if failures:
        print("Galaxy import check failed:", file=sys.stderr)
        for item in failures:
            print(f"  ERROR: {item}", file=sys.stderr)
        return 1

    print("Galaxy import check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
