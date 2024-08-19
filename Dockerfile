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

FROM qgis/qgis:release-3_16

COPY . /wtss_qgis

WORKDIR /wtss_qgis

RUN pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
        && pip3 install testresources \
            && pip3 install -e .[all]

RUN cd wtss_plugin \
    && pb_tool deploy -y --plugin_path /usr/share/qgis/python/plugins
