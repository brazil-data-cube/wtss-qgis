..
    This file is part of Python QGIS Plugin for WTSS.
    Copyright (C) 2024 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


Installation
============

The Python QGIS Plugin for WTSS depends essentially on:

- `QGIS version +3 <https://qgis.org/en/site/>`_
- `QT Creator version +5 <https://www.qt.io/download>`_
- `Python version +3 <https://www.python.org/>`_


For development environment you will need the requirements, to deploy and publish QGIS Python plugin:

- `Plugin Build Tool (pb_tool) <https://pypi.org/project/pb-tool/>`_
- `Python Test Library (pytest) <https://pypi.org/project/pytest/>`_


The fisrt step is to clone the software repository or download the zip file for `wtss_plugin`:

.. code-block:: shell

    $ git clone https://github.com/brazil-data-cube/wtss-qgis


If you clone the repository from git you needd to go to the source code folder:

.. code-block:: shell

    $ cd wtss-plugin


The next step is to install requirements and deploy the plugin in QGIS software according to your operating system.

Linux
-----

If you cloned the repository, you can install the requirements running `pip` in source code:

.. code-block:: shell

    $ pip3 install -e .[all]


Or if you download to install by `zip` file, use:

.. code-block:: shell

    $ pip3 install git+https://github.com/brazil-data-cube/wtss-qgis.git@v0.2.0


For **development environment**, go to the source code folder:

.. code-block:: shell

    $ cd wtss_plugin


In source code folder, use ``pb_tool`` to compile and deploy the plugin in Linux:

.. code-block:: shell

    $ pb_tool compile


The `pb_tool compile` will generate a file named `resources.py`, check this file before deploy:

.. code-block:: shell

    $ pb_tool deploy --plugin_path \
        /home/${USER}/.local/share/QGIS/QGIS3/profiles/default/python/plugins


Windows
-------

To install the plugin in Windows environment, with a installed version +3 for QGIS, open the Terminal as administrator and set the environment variables to link `PYTHONHOME` in QGIS:

Find the `Python` and `Grass` version installed by QGIS:

.. code-block:: text

   \wtss-qgis> dir "%OSGEO4W_ROOT%"\apps


.. code-block:: text

   \wtss-qgis> dir "%OSGEO4W_ROOT%"\apps\grass


You can set the environment variables in panel control or run the script in  `set_pyqgis_win <./scripts/set_pyqgis_win.cmd>`_.

In script its required to set the python and grass version.

For examples set the python version like `3.12` to `312` and grass version `8.4` to `84`:

.. code-block:: text

    @echo off
    set PYTHON_VERSION=312
    set GRASS_VERSION=84
    set OSGEO4W_ROOT=C:\OSGeo4W


If you download to install by `zip` file, use:

.. code-block:: shell

    \> pip3 install git+https://github.com/brazil-data-cube/wtss-qgis.git@v0.1.0


If you cloned the repository, for **development environment**, you can install the requirements running `pip` in source code:

.. code-block:: shell

    \wtss-qgis> pip3 install -e .[all]


On prompt use ``pb_tool`` to compile the plugin and generate the `resources.py`:

.. code-block:: shell

    \wtss-qgis\wtss_plugin> pb_tool compile


To deploy the plugin in Windows, go to `wtss_plugin` folder and run the script `deploy_win <./scripts/deploy_win.cmd>`_, but before set the `USER` variable to use your windows user:

.. code-block:: text

    \wtss-qgis\wtss_plugin> set USER=<your_user>


.. code-block:: shell

    \wtss-qgis\wtss_plugin> .\scripts\deploy_win.cmd


QGIS
----

The final step is run QGIS and open the Plugin Manager and enable the WTSS or for **development environment** use `Plugin Reloader`.


.. note::

    Some issues in Windows environment are related to QGIS and its `Python` installed path.

    The Python IDLE in QGIS may raise this type of errors:

    .. code-block:: text

        Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
        ModuleNotFoundError: No module named 'gdal'


    To solve this errors, add Python to the environmental variables in QGIS (`Settings >> Options >> System >> Environment`).

    The python home and path are usually like this (Using the Python 3.12):

    .. code-block:: text

        PYTHONHOME => C:\OSGeo4W\apps\Python312
        PYTHONPATH => C:\OSGeo4W\apps\qgis\python
