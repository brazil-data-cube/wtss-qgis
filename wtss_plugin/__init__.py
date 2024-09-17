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
from pathlib import Path

def lib_path():
    """Get the path for python installed lib path."""
    return str(Path(os.path.abspath(os.path.dirname(__file__))) / 'lib')

def lib_path_end():
    """Get the path for python installed lib path."""
    return str(os.path.join(str(Path(os.path.abspath(os.path.dirname(__file__))) / 'lib'), ''))

def get_lib_paths():
    """Get the path for python installed lib path."""
    return [lib_path(), lib_path_end()]

def requirements_file():
    """Get the path for requirements file."""
    return str(Path(os.path.abspath(os.path.dirname(__file__))) / 'requirements.txt')

def warning(title, message):
    """Show a simple warning when ImportError."""
    from PyQt5.QtWidgets import QMessageBox
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    return msg.exec_()

def set_lib_path():
    """Setting lib path for installed libraries."""
    import sys
    if lib_path() in sys.path:
        sys.path.remove(lib_path())
    if lib_path_end() in sys.path:
        sys.path.remove(lib_path_end())
    sys.path = get_lib_paths() + sys.path

def start(iface):
    """Start WTSS QGIS Plugin"""
    #
    # Setting PYTHONPATH to use dependencies
    set_lib_path()
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
    except (ModuleNotFoundError, ImportError) as error:
        ok_install_requirements = warning(
            "ImportError!",
            ("Your environment does not have the minimal " +
            "requirements to run WTSS Plugin, " +
            "click OK to install them.\n\n" + str(error))
        )
        if ok_install_requirements:
            import subprocess
            try:
                subprocess.run([
                    'pip', 'uninstall',
                    '-r', requirements_file(),
                ])
            except:
                pass
            subprocess.run([
                'pip', 'install',
                '--target', lib_path(),
                '-r', requirements_file(),
            ])
            ok_restart = warning(
                "Restart Required!",
                "Restart your QGIS environment to load updates!"
            )
            if ok_restart:
                import sys
                python = sys.executable
                os.execl(python, python, *sys.argv)
            else:
                return None
            return start(iface)
        else:
            return None
