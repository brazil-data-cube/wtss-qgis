# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'brazildatacube@dpi.inpe.br'
__date__ = '2019-05-04'
__copyright__ = 'Copyright 2020, INPE'

import unittest
from pathlib import Path

from jsonschema import validate
from qgis.PyQt.QtGui import QIcon

from wtss_plugin.dependencies.config import Config
from wtss_plugin.dependencies.schemas import services_storage_schema
from wtss_plugin.dependencies.wtss_qgis_controller import Services


class wtss_qgisResourcesTest(unittest.TestCase):
    """Test resources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_icon_png(self):
        """Test we can click OK."""
        path = str(Path(Config.BASE_DIR) / 'icon.png')
        icon = QIcon(path)
        self.assertFalse(icon.isNull())

    def test_01_services_storage_JSON(self):
        """Test storage of services in JSON File"""
        services_controlls = Services(user = "test")
        services_storage = services_controlls.getServicesDict()
        validate(instance = services_storage, schema = services_storage_schema)

    def test_02_list_of_services(self):
        """Test list of services"""
        services_controlls = Services(user = "test")
        list_services_names = services_controlls.getServiceNames()
        self.assertIn('E-sensing', list_services_names)

    def test_03_remove_an_existent_service(self):
        """Test if the controll is able to remove an existent service"""
        services_controlls = Services(user = "test")
        services_controlls.deleteService('E-sensing')
        list_services_names = services_controlls.getServiceNames()
        self.assertNotIn('E-sensing', list_services_names)

    def test_04_save_a_new_service(self):
        """Test if the controll is able to save a new service"""
        services_controlls = Services(user = "test")
        services_controlls.addService("New E-sensing", "http://www.esensing.dpi.inpe.br/")
        list_services_names = services_controlls.getServiceNames()
        self.assertIn('New E-sensing', list_services_names)

    def test_05_edit_an_existent_service(self):
        """Test if the controll is able to edit an existent service"""
        services_controlls = Services(user = "test")
        services_controlls.deleteService('New E-sensing')
        services_controlls.editService("E-sensing","http://www.esensing.dpi.inpe.br/")
        list_services_names = services_controlls.getServiceNames()
        self.assertIn('E-sensing', list_services_names)

if __name__ == "__main__":
    suite = unittest.makeSuite(wtss_qgisResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

