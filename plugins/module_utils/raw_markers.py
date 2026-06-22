# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

_RAW_WRAPPER_PATTERN = re.compile(
    r"^\s*\{%-?\s*raw\s*-?%}\s*\n?(.*?)\n?\s*\{%-?\s*endraw\s*-?%}\s*$",
    re.DOTALL,
)


def contains_template_marker_syntax(text):
    """True when scalar may be re-templated by Ansible or confuse Jinja (ERB, Jinja2)."""
    if not isinstance(text, str):
        return False
    return any(marker in text for marker in ("<%", "%>", "{{", "{%", "{#"))


def unwrap_jinja_raw_markers(text, preserve_template_markers=False):
    """Strip export-template raw/endraw wrappers unless ERB/Jinja markers require keeping them."""
    if not isinstance(text, str):
        return text
    match = _RAW_WRAPPER_PATTERN.match(text)
    if not match:
        return text
    inner = match.group(1)
    if preserve_template_markers and contains_template_marker_syntax(inner):
        return text
    return inner
