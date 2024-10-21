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

import importlib
import os
import platform
import sys
from pathlib import Path

import pip
from PyQt5.QtWidgets import QCheckBox, QMessageBox

WINDOWS = (
    str(platform.uname().system).lower() == 'windows'
)

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
    return str(Path(os.path.abspath(os.path.dirname(__file__))) / f'requirements.txt')

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
        checkbox.setChecked(False)
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
    if lib_path() in sys.path:
        sys.path.remove(lib_path())
    if lib_path_end() in sys.path:
        sys.path.remove(lib_path_end())
    os.environ['PYTHONPATH_WTSS_PLUGIN'] = ':'.join(sys.path)
    sys.path = get_lib_paths() + sys.path

def pip_install(
        pkg_name, pkg_version_rule,
        options=[], upgrade=False,
        reinstall=False, break_=False
    ):
    """Install the requires using pip install."""
    if upgrade:
        options.append('--upgrade')
    if reinstall:
        options.append('--force-reinstall')
    if break_:
        options.append('--break-system-packages')
    pip.main(
        ['install'] + options +
        [f"{pkg_name}{pkg_version_rule}"]
    )

def format_(name, to_import=False):
    name_ = name.replace('-', '_').replace('<=', '-')  \
        .replace('>=', '-').replace('!=', '-')  \
            .replace('<', '-').replace('>', '-') \
                .split('-')
    if not to_import:
        name_[0] = name_[0].replace('_', '-')
    return name_

def get_pkg_name(package, to_import=False):
    return format_(package, to_import)[0]

def get_pkg_version_rule(package):
    return package.split(get_pkg_name(package))[1]

def get_pkg_versions(package):
    versions = get_pkg_version_rule(package).split(',')
    versions_ = []
    for version in versions:
        version_ = format_(version)[1]
        versions_.append(float('.'.join(version_.split('.')[0:2])))
    return versions_

def run_install_pkgs_process(error_msg=""):
    """Run subprocess to install packages through."""
    install_requirements, checkbox, buttons = warning(
        "error",
        "ImportError!",
        (f"{error_msg}\n\n" +
        "Your environment does not have the minimal " +
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
        pip.main(['install', '-r', requirements_file()] + target)
        #
        # Request restart
        raise_restart()
        #
    elif install_requirements.clickedButton() == buttons['install_by']:
        with open(requirements_file(), 'r', newline='') as requirements:
            requirements = str(requirements.read()).split('\n')
            for row in requirements:
                if len(row) > 0:
                    pkg_name = get_pkg_name(row)
                    pkg_required_versions = get_pkg_versions(row)
                    pkg_version_rule = get_pkg_version_rule(row)
                    error_msg = ""
                    pkg = None
                    pkg_installed_version = None
                    try:
                        pkg = importlib.import_module(get_pkg_name(row, to_import=True))
                        pkg_installed_version = float('.'.join(pkg.__version__.split('.')[0:2]))
                    except Exception as error:
                        error_msg = str(error)
                        pass
                    if pkg_installed_version and any(pkg_installed_version < version for version in pkg_required_versions):
                        install_existing_lib, _, buttons_lib = warning(
                            "warning",
                            "Found conflicts!",
                            (f"Found existing installation for {pkg_name} version {pkg.__version__} in" +
                                f"\n\n{pkg.__file__}.\n\n" +
                                f"The WTSS Plugin needs version {pkg_version_rule}."),
                            update = ['Update', QMessageBox.YesRole],
                            cancel = ['Cancel', QMessageBox.RejectRole]
                        )
                        if install_existing_lib.clickedButton() == buttons_lib['update']:
                            pip_install(pkg_name, pkg_version_rule, options=target, upgrade=True, reinstall=True)
                        else:
                            pass
                    elif pkg == None:
                        install_lib, _, buttons_lib = warning(
                            "warning",
                            "ImportError!",
                            (f"{error_msg}\n\nThe WTSS Plugin needs package {pkg_name} version {pkg_version_rule}."),
                            install = ['Install', QMessageBox.YesRole],
                            cancel = ['Cancel', QMessageBox.RejectRole]
                        )
                        if install_lib.clickedButton() == buttons_lib['install']:
                            pip_install(pkg_name, pkg_version_rule, options=target)
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
        run_install_pkgs_process(error_msg=error)
        #
        return start(iface)
