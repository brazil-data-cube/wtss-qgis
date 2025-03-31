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
#!/bin/bash

PLUGIN_PATH=./wtss_plugin

# Remove the python cache files
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | sudo xargs rm -rf

# Get LICENSE from root
cp LICENSE ${PLUGIN_PATH}

# Go to plugin path to zip files
cd ${PLUGIN_PATH}

pb_tool zip
