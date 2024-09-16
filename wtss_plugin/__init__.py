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

def start(iface):
    """Start WTSS QGIS Plugin"""
    #
    # Setting PYTHONPATH to use dependencies
    import os
    import sys
    from pathlib import Path
    sys.path.append(str(Path(os.path.abspath(os.path.dirname(__file__))) / 'lib'))
    #
    # Start plugin GUI
    from .wtss_qgis import wtss_qgis
    return wtss_qgis(iface)

def classFactory(iface):
    """Load wtss_qgis class from file wtss_qgis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    try:
        return start(iface)
    except:
        import pip
        pip.main([
            'install',
            '-r', 'requirements.txt',
            '--target', 'lib'
        ])
        return start(iface)
