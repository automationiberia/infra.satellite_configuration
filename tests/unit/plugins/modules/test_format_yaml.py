from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""Unit tests for the format_yaml module helpers."""

import importlib.util
import pathlib
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
MODULE_PATH = REPO_ROOT / "plugins" / "modules" / "format_yaml.py"
RAW_MARKERS_PATH = REPO_ROOT / "plugins" / "module_utils" / "raw_markers.py"
SPEC = importlib.util.spec_from_file_location("format_yaml", MODULE_PATH)
FORMAT_YAML = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FORMAT_YAML)
RAW_SPEC = importlib.util.spec_from_file_location("raw_markers", RAW_MARKERS_PATH)
RAW_MARKERS = importlib.util.module_from_spec(RAW_SPEC)
RAW_SPEC.loader.exec_module(RAW_MARKERS)


class TestCleanYamlTreeCryptoRepair(unittest.TestCase):
    def test_unwraps_jinja_raw_markers(self):
        wrapped = "{% raw %}\nPurpose: default administrator\n{% endraw %}"
        self.assertEqual(RAW_MARKERS.unwrap_jinja_raw_markers(wrapped), "Purpose: default administrator")

    def test_preserves_raw_wrapper_for_erb_content(self):
        wrapped = "{% raw %}\n<% host.name %>\n{% endraw %}"
        self.assertEqual(
            RAW_MARKERS.unwrap_jinja_raw_markers(wrapped, preserve_template_markers=True),
            wrapped,
        )

    def test_repairs_flattened_crypto_key_when_auto_block_false(self):
        flattened_pem = "-----BEGIN CERTIFICATE----- LINEONE LINETWO LINETHREE -----END CERTIFICATE-----"
        tree = {"cert": flattened_pem}

        FORMAT_YAML.clean_yaml_tree(tree, auto_block=False)

        repaired_value = tree["cert"]
        self.assertIn("\n", repaired_value)
        self.assertIn("-----BEGIN CERTIFICATE-----\n", repaired_value)
        self.assertIn("\n-----END CERTIFICATE-----", repaired_value)

    def test_repairs_flattened_crypto_key_in_list_when_auto_block_false(self):
        flattened_key = "-----BEGIN PRIVATE KEY----- AAAABBBB CCCC -----END PRIVATE KEY-----"
        tree = [flattened_key]

        FORMAT_YAML.clean_yaml_tree(tree, auto_block=False)

        repaired_value = tree[0]
        self.assertIn("\n", repaired_value)
        self.assertIn("-----BEGIN PRIVATE KEY-----\n", repaired_value)
        self.assertIn("\n-----END PRIVATE KEY-----", repaired_value)


if __name__ == "__main__":
    unittest.main()
