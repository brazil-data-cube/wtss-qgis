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

QGIS_PREFIX_PATH=/usr/local/qgis-2.0
if [ -n "$1" ]; then
    QGIS_PREFIX_PATH=$1
fi

echo ${QGIS_PREFIX_PATH}


export QGIS_PREFIX_PATH=${QGIS_PREFIX_PATH}
export QGIS_PATH=${QGIS_PREFIX_PATH}
export LD_LIBRARY_PATH=${QGIS_PREFIX_PATH}/lib
export PYTHONPATH=${QGIS_PREFIX_PATH}/share/qgis/python:${QGIS_PREFIX_PATH}/share/qgis/python/plugins:${PYTHONPATH}

echo "QGIS PATH: $QGIS_PREFIX_PATH"
export QGIS_DEBUG=0
export QGIS_LOG_FILE=/tmp/inasafe/realtime/logs/qgis.log

export PATH=${QGIS_PREFIX_PATH}/bin:$PATH

echo "This script is intended to be sourced to set up your shell to"
echo "use a QGIS 2.0 built in $QGIS_PREFIX_PATH"
echo
echo "To use it do:"
echo "source $BASH_SOURCE /your/optional/install/path"
echo
echo "Then use the make file supplied here e.g. make guitest"
