#!/usr/bin/env python3
"""Local checks mirroring galaxy-importer / ansible-test Python sanity rules."""

from __future__ import annotations

import ast
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GALAXY = REPO_ROOT / "galaxy.yml"
COLLECTION_PYTHON_DIRS = ("plugins", "tests")
FUTURE_IMPORT = "from __future__ import absolute_import, division, print_function"
METACLASS = "__metaclass__ = type"


def _load_collection_identity():
    namespace = None
    name = None
    for line in GALAXY.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("namespace:"):
            namespace = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("name:"):
            name = stripped.split(":", 1)[1].strip()
    if not namespace or not name:
        raise RuntimeError("Could not read namespace/name from galaxy.yml")
    return namespace, name


def _iter_python_files():
    for base in COLLECTION_PYTHON_DIRS:
        root = REPO_ROOT / base
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.py")):
            yield path


def _check_future_import_and_metaclass(path: Path, source: str) -> list[str]:
    errors = []
    if FUTURE_IMPORT not in source:
        errors.append(f"{path}: missing ansible future-import boilerplate")
    if METACLASS not in source:
        errors.append(f"{path}: missing ansible metaclass boilerplate")
    return errors


def _check_fstring_backslash_compat(path: Path, source: str, tree: ast.AST) -> list[str]:
    errors = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.JoinedStr):
            continue
        for part in node.values:
            if not isinstance(part, ast.FormattedValue):
                continue
            expr_source = ast.get_source_segment(source, part.value)
            if expr_source and "\\" in expr_source:
                errors.append(
                    f"{path}:{node.lineno}:{node.col_offset}: "
                    f"f-string expression contains a backslash (invalid before Python 3.12): {expr_source!r}"
                )
    return errors


def _check_python_files() -> list[str]:
    errors = []
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path}:{exc.lineno}:{exc.offset}: syntax-error: {exc.msg}")
            continue

        errors.extend(_check_future_import_and_metaclass(path, source))
        errors.extend(_check_fstring_backslash_compat(path, source, tree))
    return errors


def _check_ansible_doc(namespace: str, name: str) -> list[str]:
    if not shutil_which("ansible-doc"):
        return []

    fqcn = f"{namespace}.{name}.format_yaml"
    with tempfile.TemporaryDirectory(prefix="ansible-collections-") as tmp_dir:
        collection_root = Path(tmp_dir) / "ansible_collections" / namespace / name
        collection_root.parent.mkdir(parents=True, exist_ok=True)
        collection_root.symlink_to(REPO_ROOT, target_is_directory=True)

        env = os.environ.copy()
        env["ANSIBLE_COLLECTIONS_PATH"] = tmp_dir
        env.pop("ANSIBLE_COLLECTIONS_PATHS", None)
        env["ANSIBLE_LOCAL_TEMP"] = os.path.join(tmp_dir, "ansible-local")
        os.makedirs(env["ANSIBLE_LOCAL_TEMP"], exist_ok=True)

        result = subprocess.run(
            ["ansible-doc", "--type", "module", "--json", fqcn],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return []

        detail = (result.stderr or result.stdout or "ansible-doc failed").strip()
        return [f"ansible-doc {fqcn}: {detail}"]


def shutil_which(command: str) -> str | None:
    for path in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path) / command
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def main() -> int:
    errors = _check_python_files()
    try:
        namespace, name = _load_collection_identity()
        errors.extend(_check_ansible_doc(namespace, name))
    except RuntimeError as exc:
        errors.append(str(exc))

    if errors:
        print("Collection Python sanity check failed:", file=sys.stderr)
        for error in errors:
            print(f"  ERROR: {error}", file=sys.stderr)
        return 1

    print("Collection Python sanity check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
