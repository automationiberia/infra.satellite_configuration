# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def merge_list_by_key(base, overrides, merge_key="name"):
    """Merge override objects into a base list by merge_key; overrides win on collision."""
    if not isinstance(base, list):
        base = []
    if not isinstance(overrides, list):
        overrides = []

    override_by_key = {}
    for item in overrides:
        if isinstance(item, dict) and merge_key in item:
            override_by_key[item[merge_key]] = item

    merged = []
    seen_keys = set()
    for item in base:
        if not isinstance(item, dict):
            merged.append(item)
            continue
        key = item.get(merge_key)
        if key in override_by_key:
            merged.append(override_by_key[key])
            seen_keys.add(key)
        else:
            merged.append(item)

    for item in overrides:
        if not isinstance(item, dict) or merge_key not in item:
            continue
        key = item[merge_key]
        if key not in seen_keys:
            merged.append(item)
            seen_keys.add(key)

    return merged
