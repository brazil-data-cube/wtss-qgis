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

__author__ = 'brazildatacube@dpi.inpe.br'
__date__ = '2019-05-04'
__copyright__ = 'Copyright 2020, INPE'

import unittest

from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from wtss_plugin.controller.wtss_qgis_controller import Services
from wtss_plugin.wtss_qgis_dialog import wtss_qgisDialog

from .utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class wtss_qgisDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.dialog = wtss_qgisDialog(None)

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_01_comboBox_select_services(self):
        """Test we can select a service from WTSS available servers."""
        self.server_controlls = Services(user = "test")
        comboBox = self.dialog.service_selection
        comboBox.addItems(self.server_controlls.getServiceNames())
        allItems = [comboBox.itemText(i) for i in range(comboBox.count())]
        data_exists = len(allItems) > 0
        self.assertEqual(data_exists, True)

if __name__ == "__main__":
    suite = unittest.makeSuite(wtss_qgisDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
