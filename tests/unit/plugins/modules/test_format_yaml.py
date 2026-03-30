import importlib.util
import pathlib
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
MODULE_PATH = REPO_ROOT / "plugins" / "modules" / "format_yaml.py"
SPEC = importlib.util.spec_from_file_location("format_yaml", MODULE_PATH)
FORMAT_YAML = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FORMAT_YAML)


class TestCleanYamlTreeCryptoRepair(unittest.TestCase):
    def test_repairs_flattened_crypto_key_when_auto_block_false(self):
        flattened_pem = "-----BEGIN CERTIFICATE----- " "LINEONE LINETWO LINETHREE " "-----END CERTIFICATE-----"
        tree = {"cert": flattened_pem}

        FORMAT_YAML.clean_yaml_tree(tree, auto_block=False)

        repaired_value = tree["cert"]
        self.assertIn("\n", repaired_value)
        self.assertIn("-----BEGIN CERTIFICATE-----\n", repaired_value)
        self.assertIn("\n-----END CERTIFICATE-----", repaired_value)

    def test_repairs_flattened_crypto_key_in_list_when_auto_block_false(self):
        flattened_key = "-----BEGIN PRIVATE KEY----- " "AAAABBBB CCCC " "-----END PRIVATE KEY-----"
        tree = [flattened_key]

        FORMAT_YAML.clean_yaml_tree(tree, auto_block=False)

        repaired_value = tree[0]
        self.assertIn("\n", repaired_value)
        self.assertIn("-----BEGIN PRIVATE KEY-----\n", repaired_value)
        self.assertIn("\n-----END PRIVATE KEY-----", repaired_value)


if __name__ == "__main__":
    unittest.main()
