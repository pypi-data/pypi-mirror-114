# Calliope
# Copyright (C) 2021  Kilian Lackhove <kilian@lackhove.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Utility functions for resolving items
"""

import re
from datetime import date
from typing import Iterable, Optional, Dict

from calliope.playlist import Item


def normalize_artist_title(
    artist: Optional[str], title: Optional[str]
) -> tuple[Optional[str], Optional[str]]:
    """
    Remove featuring artists from title and append them to the artist string
    """
    feat_artist = None
    if title is not None:
        m = re.match(r"(.*?)\(?feat\.(.*)\)?", title, flags=re.IGNORECASE)
        if m is not None:
            title = m.group(1).strip()
            feat_artist = m.group(2).strip()

    if artist is not None:
        if artist.casefold().endswith(", the"):
            artist = "The " + artist[:-5]
        if feat_artist is not None:
            artist = (artist + " " + feat_artist).strip()

    return artist, title


def drop_none_values(dct: Item) -> Item:
    """
    Delete all fields with None value from dct.
    """
    drop_keys = []
    for k, v in dct.items():
        if v is None:
            drop_keys.append(k)

    for k in drop_keys:
        del dct[k]

    return dct


def parse_sort_date(date_str: Optional[str]) -> Optional[date]:
    """
    Parse a potentially incomplete date string of the format YYYY-MM-DD and
    return a datetime.date object with conservative defaults for missing data.
    """
    if date_str is None:
        return None

    try:
        ymd = [int(e) for e in date_str.split("-") if e != ""]
    except ValueError:
        return None
    if len(ymd) < 1:
        return None
    if len(ymd) < 2:
        ymd.append(12)
    if len(ymd) < 3:
        ymd.append(28)

    try:
        return date(*(int(v) for v in ymd))
    except ValueError:
        return None


def get_nested(sequence: Dict, keys: Iterable):
    """
    Get the value from a nested dict/list data structure, returning None if one
    of the keys is invalid.
    """
    current = sequence
    for key in keys:
        try:
            current = current[key]
        except (KeyError, IndexError):
            return None

    return current
