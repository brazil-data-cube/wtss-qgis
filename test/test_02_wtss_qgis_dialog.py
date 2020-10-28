# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'brazildatacube@dpi.inpe.br'
__date__ = '2020-05-04'
__copyright__ = 'Copyright 2020, INPE'

import unittest

from qgis.PyQt.QtWidgets import QDialog, QDialogButtonBox

from wtss_plugin import Services
from wtss_qgis_dialog import wtss_qgisDialog

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

    def test_dialog_ok(self):
        """Test we can click OK."""
        button = self.dialog.dialogButtonBox.button(QDialogButtonBox.Ok)
        button.click()
        result = self.dialog.result()
        self.assertEqual(result, QDialog.Accepted)

    def test_dialog_cancel(self):
        """Test we can click cancel."""
        button = self.dialog.dialogButtonBox.button(QDialogButtonBox.Cancel)
        button.click()
        result = self.dialog.result()
        self.assertEqual(result, QDialog.Rejected)

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
