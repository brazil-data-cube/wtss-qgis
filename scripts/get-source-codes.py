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

"""Python Script to list Path libraries."""

from pathlib import Path

lib_paths = []

import json

lib_paths.append(json.__file__)

import numpy

lib_paths.append(numpy.__file__)

import seaborn

lib_paths.append(seaborn.__file__)

import matplotlib

lib_paths.append(matplotlib.__file__)

import pandas

lib_paths.append(pandas.__file__)

import jsonschema

lib_paths.append(jsonschema.__file__)

import pystac

lib_paths.append(pystac.__file__)

import pystac_client

lib_paths.append(pystac_client.__file__)

import wtss

lib_paths.append(wtss.__file__)

file = open(Path('scripts') / 'lib-paths.txt', 'w')
for path in lib_paths:
	file.write(str(path).replace('__init__.py', '') + "\n")
file.close()
