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

from .helpers.installation_helper import InstallDependencies

installDependencies = InstallDependencies(__file__)

def classFactory(iface):
    """Load wtss_qgis class from file wtss_qgis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    # Setting PYTHONPATH to use dependencies
    installDependencies.set_lib_path()
    try:
        #
        # Test import of dependencies
        from .wtss_qgis import WTSSQgis
    except (ModuleNotFoundError, ImportError) as error:
        #
        # Run packages installation
        installDependencies.run_install_pkgs_process(error_msg=error)
        #
        # Test imports of dependencies again
        from .wtss_qgis import WTSSQgis
    #
    # Start plugin GUI
    return WTSSQgis(iface)
