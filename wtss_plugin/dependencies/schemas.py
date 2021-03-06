"""
WTSS QGIS Plugin.

Python Client Library for Web Time Series Service.
Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/.
                              -------------------
begin                : 2019-05-04
git sha              : $Format:%H$
copyright            : (C) 2020 by INPE
email                : brazildatacube@dpi.inpe.br

This program is free software.

You can redistribute it and/or modify it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
"""


from json import loads as json_loads
from pathlib import Path

from .config import Config

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
