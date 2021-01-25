"""Common functionality used by regression tests."""

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
    """ Start one QGIS application to test against.

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
