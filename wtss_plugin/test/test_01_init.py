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

__author__ = 'Tim Sutton <tim@linfiniti.com>'
__revision__ = '$Format:%H$'
__date__ = '17/10/2010'
__license__ = "GPL"
__copyright__ = 'Copyright 2012, Australia Indonesia Facility for '
__copyright__ += 'Disaster Reduction'

import configparser
import logging
import os
import unittest

LOGGER = logging.getLogger('QGIS')


class TestInit(unittest.TestCase):
    """Test that the plugin init is usable for QGIS.

    Based heavily on the validator class by Alessandro
    Passoti available here:

    http://github.com/qgis/qgis-django/blob/master/qgis-app/
             plugins/validator.py

    """

    def test_read_init(self):
        """Test that the plugin __init__ will validate on plugins.qgis.org."""

        # You should update this list according to the latest in
        # https://github.com/qgis/qgis-django/blob/master/qgis-app/
        #        plugins/validator.py

        required_metadata = [
            'name',
            'description',
            'version',
            'qgisMinimumVersion',
            'email',
            'author']

        file_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), os.pardir,
            'metadata.txt'))
        LOGGER.info(file_path)
        metadata = []
        parser = configparser.ConfigParser()
        parser.optionxform = str
        parser.read(file_path)
        message = 'Cannot find a section named "general" in %s' % file_path
        assert parser.has_section('general'), message
        metadata.extend(parser.items('general'))

        for expectation in required_metadata:
            message = ('Cannot find metadata "%s" in metadata source (%s).' % (
                expectation, file_path))

            self.assertIn(expectation, dict(metadata), message)

if __name__ == '__main__':
    unittest.main()
