# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from ansible_collections.infra.satellite_configuration.plugins.module_utils.merge_overrides import (
        merge_list_by_key,
    )
except ModuleNotFoundError:
    import importlib.util
    from pathlib import Path

    _MERGE_OVERRIDES_PATH = Path(__file__).resolve().parent.parent / "module_utils" / "merge_overrides.py"
    _MERGE_SPEC = importlib.util.spec_from_file_location("merge_overrides", _MERGE_OVERRIDES_PATH)
    _MERGE_MODULE = importlib.util.module_from_spec(_MERGE_SPEC)
    _MERGE_SPEC.loader.exec_module(_MERGE_MODULE)
    merge_list_by_key = _MERGE_MODULE.merge_list_by_key


class FilterModule:
    """Filters for merging environment-specific CaC overrides."""

    def filters(self):
        return {
            "satellite_configuration_merge_by_key": self.satellite_configuration_merge_by_key,
        }

    def satellite_configuration_merge_by_key(self, base, overrides, merge_key="name"):
        return merge_list_by_key(base, overrides, merge_key)
