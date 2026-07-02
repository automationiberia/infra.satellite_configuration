# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import importlib.util
import pathlib
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
MERGE_OVERRIDES_PATH = REPO_ROOT / "plugins" / "module_utils" / "merge_overrides.py"
SPEC = importlib.util.spec_from_file_location("merge_overrides", MERGE_OVERRIDES_PATH)
MERGE_OVERRIDES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MERGE_OVERRIDES)


class TestMergeListByKey(unittest.TestCase):
    def test_replaces_matching_objects(self):
        base = [{"name": "a", "value": 1}, {"name": "b", "value": 2}]
        overrides = [{"name": "b", "value": 99}]
        self.assertEqual(
            MERGE_OVERRIDES.merge_list_by_key(base, overrides),
            [{"name": "a", "value": 1}, {"name": "b", "value": 99}],
        )

    def test_appends_new_override_objects(self):
        base = [{"name": "a", "value": 1}]
        overrides = [{"name": "b", "value": 2}]
        self.assertEqual(
            MERGE_OVERRIDES.merge_list_by_key(base, overrides),
            [{"name": "a", "value": 1}, {"name": "b", "value": 2}],
        )

    def test_handles_empty_base(self):
        overrides = [{"name": "only", "value": 1}]
        self.assertEqual(MERGE_OVERRIDES.merge_list_by_key([], overrides), overrides)


if __name__ == "__main__":
    unittest.main()
