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

import csv
import importlib
import os
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox, QCheckBox


def lib_path():
    """Get the path for python installed lib path."""
    return str(Path(os.path.abspath(os.path.dirname(__file__))) / 'lib')

def lib_path_end():
    """Get the path for python installed lib path."""
    return str(os.path.join(str(Path(os.path.abspath(os.path.dirname(__file__))) / 'lib'), ''))

def get_lib_paths():
    """Get the path for python installed lib path."""
    return [lib_path(), lib_path_end()]

def requirements_file(ext):
    """Get the path for requirements file."""
    return str(Path(os.path.abspath(os.path.dirname(__file__))) / f'requirements.{ext}')

def warning(type_message, title, message, checkbox = None, **add_buttons):
    """Show a simple warning when ImportError."""
    msg = QMessageBox()
    if type_message == 'error':
        msg.setIcon(QMessageBox.Critical)
    elif type_message == 'warning':
        msg.setIcon(QMessageBox.Warning)
    elif type_message == 'info':
        msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(title)
    msg.setText(message)
    buttons = {}
    if add_buttons:
        for button in add_buttons.keys():
            buttons[button] = msg.addButton(add_buttons[button][0], add_buttons[button][1])
    if checkbox:
        checkbox.setChecked(True)
        msg.setCheckBox(checkbox)
    msg.exec_()
    msg.deleteLater()
    return msg, checkbox, buttons

def raise_restart():
    """Raise a warning requesting restart."""
    restart, _, buttons_ = warning(
        "warning",
        "Restart Required!",
        "Restart your QGIS environment to load updates!",
        ok = ['Ok', QMessageBox.YesRole],
        cancel = ['Cancel', QMessageBox.RejectRole]
    )
    if restart.clickedButton() == buttons_['ok']:
        import sys
        python = sys.executable
        os.execl(python, python, *sys.argv)

def set_lib_path():
    """Setting lib path for installed libraries."""
    import sys
    if lib_path() in sys.path:
        sys.path.remove(lib_path())
    if lib_path_end() in sys.path:
        sys.path.remove(lib_path_end())
    sys.path = get_lib_paths() + sys.path

def run_install_pkgs_process():
    """Run subprocess to install packages through."""
    install_requirements, checkbox, buttons = warning(
        "error",
        "ImportError!",
        ("Your environment does not have the minimal " +
        "requirements to run WTSS Plugin, " +
        "click OK to install them."),
        checkbox = QCheckBox("Use python home?"),
        install_all = ['Install All', QMessageBox.YesRole],
        install_by = ['Install By', QMessageBox.YesRole],
        cancel = ['Cancel', QMessageBox.RejectRole]
    )
    target = []
    if not checkbox.isChecked():
        target = ['--target', lib_path()]
    if install_requirements.clickedButton() == buttons['install_all']:
        subprocess.run(
            [
                'pip', 'install', '--upgrade',
                '-r', requirements_file('txt')
            ] + target,
            shell = True
        )
        #
        # Request restart
        raise_restart()
        #
    elif install_requirements.clickedButton() == buttons['install_by']:
        with open(requirements_file('csv'), newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                pkg_name = row['package']
                pkg_required_version = float('.'.join(row['version'].split('.')[0:2]))
                pkg = None
                try:
                    pkg = importlib.import_module(pkg_name)
                except (ModuleNotFoundError, ImportError) as error:
                    pass
                pkg_installed_version = None
                if pkg:
                    pkg_installed_version = float('.'.join(pkg.__version__.split('.')[0:2]))
                if pkg_installed_version and pkg_required_version >= pkg_installed_version:
                    install_existing_lib, _, buttons_lib = warning(
                        "warning",
                        "Found conflicts!",
                        (f"Found existing installation for {pkg_name} version {pkg.__version__} in" +
                            f"\n\n{pkg.__file__}.\n\n" +
                            f"The WTSS Plugin needs version >= {pkg_required_version}."),
                        update = ['Update', QMessageBox.YesRole],
                        cancel = ['Cancel', QMessageBox.RejectRole]
                    )
                    if install_existing_lib.clickedButton() == buttons_lib['update']:
                        subprocess.run(
                            ['pip', 'install'] + target +
                            ['--upgrade'] +
                            [f"{pkg_name}>={pkg_required_version}"],
                            shell = True
                        )
                    else:
                        pass
                elif pkg == None:
                    install_lib, _, buttons_lib = warning(
                        "warning",
                        "ImportError!",
                        (f"The WTSS Plugin needs package {pkg_name} version >= {pkg_required_version}."),
                        install = ['Install', QMessageBox.YesRole],
                        cancel = ['Cancel', QMessageBox.RejectRole]
                    )
                    if install_lib.clickedButton() == buttons_lib['install']:
                        subprocess.run(
                            ['pip', 'install'] + target +
                            [f"{pkg_name}>={pkg_required_version}"],
                            shell = True
                        )
                    else:
                        pass
        #
        # Request restart
        raise_restart()
        #
    else:
        pass

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
        #
        # Run packages installation
        run_install_pkgs_process()
        #
        return start(iface)
