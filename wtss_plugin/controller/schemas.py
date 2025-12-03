#
# This file is part of Python QGIS Plugin for WTSS.
# Copyright (C) 2024 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Python QGIS Plugin for WTSS."""

from json import loads as json_loads
from pathlib import Path

from ..config import Config

schemas_folder = Path(Config.BASE_DIR) / 'json-schemas'

def load_schema(file_name):
    """Open file and parses as JSON file.

    :param file_name<str>: File name of JSON Schema.
    :returns: JSON schema parsed as Python object (dict).
    :raises: json.JSONDecodeError When file is not valid JSON object.
    """
    schema_file = schemas_folder / file_name

    with schema_file.open() as f:
        return json_loads(f.read())

services_storage_schema = load_schema('services_schema.json')
