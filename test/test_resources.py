# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'brazildatacube@dpi.inpe.br'
__date__ = '2020-05-04'
__copyright__ = 'Copyright 2020, INPE'

import unittest

from qgis.PyQt.QtGui import QIcon
from wtss_plugin.wtss_qgis_controller import Services


class wtss_qgisDialogTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_icon_png(self):
        """Test we can click OK."""
        path = ':/plugins/wtss_qgis/icon.png'
        icon = QIcon(path)
        self.assertFalse(icon.isNull())

    def list_of_services(self):
        """Test list of services"""
        services_controlls = Services()
        list_services_names = services_controlls.getServiceNames()
        self.assertIn('Brazil Data Cube', list_services_names)
        self.assertIn('E-sensing', list_services_names)


if __name__ == "__main__":
    suite = unittest.makeSuite(wtss_qgisResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)



