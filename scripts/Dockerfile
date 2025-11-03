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
# Build image with:
#
# docker build --build-arg FILE="wtss_plugin.zip" -t wtss_qgis/qgis:3.42 .
#

ARG QGIS_RELEASE=3.42
FROM qgis/qgis:${QGIS_RELEASE}

ARG FILE
ENV ZIP_FILE=${FILE}

ADD ${ZIP_FILE} .

RUN apt-get update && \
    apt-get install -y zip

RUN unzip ${ZIP_FILE} -d \
    /usr/share/qgis/python/plugins/

RUN python3 -m pip install --user -r \
    /usr/share/qgis/python/plugins/wtss_plugin/requirements.txt \
    --break-system-packages

RUN mkdir -p ~/.local/share/QGIS/QGIS3/profiles/default/QGIS

RUN echo -e "\n[PythonPlugins]\nwtss_plugin=true\n" \
    >> ~/.local/share/QGIS/QGIS3/profiles/default/QGIS/QGIS3.ini

CMD /bin/bash
