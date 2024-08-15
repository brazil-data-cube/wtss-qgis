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

import os

from qgis.PyQt import QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'wtss_qgis_dialog_base.ui'))

class wtss_qgisDialog(QtWidgets.QDialog, FORM_CLASS):
    """Set up the user interface from Designer through FORM_CLASS.

    :param QDialog: QDialog
    :param FORM_CLASS: Set gui
    """

    def __init__(self, parent=None):
        """Build UI element.

        :param parent: None
        """
        super(wtss_qgisDialog, self).__init__(parent)
        self.setupUi(self)
