# Calliope
# Copyright (C) 2019  Sam Thursfield <sam@afuera.me.uk>
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

import importlib


def get_resolver_module(name):
    return importlib.import_module(f"calliope.{name}")


def resolve_content(playlist, resolve_order=None):
    result = []
    for item in playlist:
        for resolver_name in resolve_order:
            module = get_resolver_module(resolver_name)
            location_property = f"{resolver_name}.location"
            try:
                resolved_item = module.resolve_content(item)
                if location_property in resolved_item:
                    resolved_item["location"] = resolved_item[location_property]
                    result.append(resolved_item)
                    break
            except Exception as e:
                raise
        else:
            result.append(item)
    return result
