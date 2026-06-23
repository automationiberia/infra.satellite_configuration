# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from ansible_collections.infra.satellite_configuration.plugins.module_utils.raw_markers import (
        sanitize_partition_table_layout,
        unwrap_jinja_raw_markers,
    )
except ModuleNotFoundError:
    import importlib.util
    from pathlib import Path

    _RAW_MARKERS_PATH = Path(__file__).resolve().parent.parent / "module_utils" / "raw_markers.py"
    _RAW_SPEC = importlib.util.spec_from_file_location("raw_markers", _RAW_MARKERS_PATH)
    _RAW_MODULE = importlib.util.module_from_spec(_RAW_SPEC)
    _RAW_SPEC.loader.exec_module(_RAW_MODULE)
    sanitize_partition_table_layout = _RAW_MODULE.sanitize_partition_table_layout
    unwrap_jinja_raw_markers = _RAW_MODULE.unwrap_jinja_raw_markers


class FilterModule:
    """Filters for CaC raw/endraw marker handling."""

    def filters(self):
        return {
            "satellite_configuration_unwrap_raw_markers": self.satellite_configuration_unwrap_raw_markers,
            "satellite_configuration_sanitize_partition_table_layout": self.satellite_configuration_sanitize_partition_table_layout,
        }

    def satellite_configuration_sanitize_partition_table_layout(self, value):
        return sanitize_partition_table_layout(value)

    def satellite_configuration_unwrap_raw_markers(self, value):
        if isinstance(value, str):
            return unwrap_jinja_raw_markers(value, preserve_template_markers=False)
        return value
