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

import logging
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import *
from qgis.gui import *

LOGGER = logging.getLogger('QGIS')
QGIS_APP = None
CANVAS = None
PARENT = None
IFACE = None


def get_qgis_app():
    """Start one QGIS application to test against.

    :returns: Handle to QGIS app, canvas, iface and parent. If there are any
        errors the tuple members will be returned as None.
    :rtype: (QgsApplication, CANVAS, IFACE, PARENT)

    If QGIS is already running the handle to that app will be returned.
    """
    global QGIS_APP
    if QGIS_APP is None:
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        QgsApplication.setPrefixPath("/usr", False)
        QGIS_APP = QgsApplication([], False)
        QGIS_APP.initQgis()
        s = QGIS_APP.showSettings()
        LOGGER.debug(s)

    global PARENT
    if PARENT is None:
        PARENT = QWidget()

    global CANVAS
    if CANVAS is None:
        CANVAS = QgsMapCanvas(PARENT)
        CANVAS.resize(QtCore.QSize(400, 400))

    return QGIS_APP, CANVAS, PARENT
