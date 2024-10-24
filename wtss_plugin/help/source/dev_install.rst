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


========================
Development Installation
========================

The Python QGIS Plugin for WTSS depends essentially on:

 - `QGIS > 3 <https://qgis.org/en/site/>`_
 - `Python > 3.10 <https://www.python.org/>`_
 - `Python QT Package > 5 <https://www.qt.io/download>`_

For **development environment**, you will need to set your python QGIS environment variables basing on your operation system. This means that your QGIS must be configured with your python variables using a terminal or CMD.

This **development environment** consist in a environment with all dependencies required to **compile** and **build** the plugin installer for WTSS QGIS Plugin.

Linux
-----

The scripts to help to configure the environment variables are located in `Linux bash scripts <../wtss-qgis/scripts/linux>`_.

The fisrt step is to clone the software repository for `wtss_plugin`:

.. code-block:: text

    $ git clone https://github.com/brazil-data-cube/wtss-qgis


If you clone the repository from git you needd to go to the source code folder:

.. code-block:: text

    $ cd wtss-qgis


The next step is to install requirements and deploy the plugin in QGIS software according to your operating system.

If you cloned the repository, you can install the requirements running `pip` in source code:

.. code-block:: text

    $ pip3 install -e .[all]


Now you will need to generate a `requirements.txt` file for plugin install and resolve dependencies conflicts in background when users get the zip file:

This is because only QGIS does not resolve external dependencies like `WTSS.py <https://github.com/brazil-data-cube/wtss.py>`_, and to generate the zip file for user installation, the requirements is needed to run installation script in `__init__.py <../wtss_plugin/__init__.py>`_.

To generate this file use this script:

.. code-block:: text

    $ python3 scripts/build_requirements.py


After `requirements.txt`, you will need to compile the `resources.qrc`, then go to the source code folder:

.. code-block:: text

    $ cd wtss_plugin


The plugin source code is located at `./wtss_plugin <../wtss_plugin>`_, this folder will be compressed to generate the final zip to user installation.

In source code folder, use `pb_tool` to compile the `requirements.qrc`. The `pb_tool compile` will generate a file named `resources.py`, check this file before deploy:

.. code-block:: text

    $ pb_tool compile


After this steps, the plugin is able to deploy and generate zip. In the development environemnt you can deploy the plugin directely to your installed QGIS.

To deploy the plugin in your installed QGIS, execute:

.. code-block:: text

    $ pb_tool deploy --plugin_path \
        /home/${USER}/.local/share/QGIS/QGIS3/profiles/default/python/plugins


To generate the zip file for plugin installer, use:

.. code-block:: text

    $ pb_tool zip


This command will compress the files configured in `pb_tool.cfg <../wtss_plugin/pb_tool.cfg>`_, any errors may be related to previous steps with the generated files `requirements.txt` and `resources.py`.

Docker
------

To run this plugin in a `QGIS Docker <https://hub.docker.com/r/qgis/qgis>`_ instance it is required a installed `Docker <https://www.docker.com/>`_ version.

There are two ways to run the plugin: building the image for plugin or run the QGIS Docker and install the user zip file.

To build the plugin image you need to run:

.. code-block:: text

    $ docker build -t wtss-qgis .


After build the plugin image, you need to run this script in the root of repository:

.. code-block:: text

    $ bash scripts/linux/run-qgis-wtss-plugin.sh


.. note::

    For Windows users, this script is detailed below:

    .. code-block:: text

        docker run --rm \
            --interactive \
            --tty \
            --name qgis-docker-wtss-plugin \
            -i -t \
            -v ${PWD}:/home/wtss_plugin \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -e DISPLAY=unix$DISPLAY \
            wtss-qgis:latest qgis


To run only the QGIS instance and after run the user installation:

.. code-block:: text

    $ QGIS_RELEASE="release-3_28" \
        bash scripts/linux/run-qgis.sh


With the QGIS instance running go to ``Plugins >> Manage and Install Plugins`` and install the plugin via zip, using the generated zip file using ``pb_tool zip`` or any compressing app.

Note that you can choose the release of QGIS, in this example was chosen the `3.28` version.

.. note::

    For Windows users, this script can be adapted from:

    .. code-block:: text

        set OSGEO4W_ROOT=release-3_28

        docker run --rm \
            --interactive \
            --tty \
            --name qgis-docker \
            -i -t \
            -v ${PWD}:/home/wtss_plugin \
            -v ${PWD}/plugins:/root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -e DISPLAY=unix$DISPLAY \
            qgis/qgis:%OSGEO4W_ROOT% qgis


Windows
-------

The scripts to help to configure the environment variables are located in `Windows CMD <../wtss-qgis/scripts/win>`_.

To install the plugin in Windows environment, with a installed version > 3 for QGIS, open the Terminal as administrator and set the environment variables to link `PYTHONHOME` in QGIS.

To set `PYTHONHOME`, find the `Python` and `Grass` version installed by QGIS, you can use this commands:

.. code-block:: text

   \wtss-qgis> dir "%OSGEO4W_ROOT%"\apps


.. code-block:: text

   \wtss-qgis> dir "%OSGEO4W_ROOT%"\apps\grass


You can set the environment variables in panel control if you were a experient windows user or run the script in `set-pyqgis-win.cmd <../../../scripts/win/set-pyqgis-win.cmd>`_.

But this script must be updated, its required to set the python and grass version. For example below set the python version like `3.12` to `312` and grass version `8.4` to `84`:

.. code-block:: text

    @echo off
    set PYTHON_VERSION=312
    set GRASS_VERSION=84
    set OSGEO4W_ROOT=C:\OSGeo4W


Now you can run the `set-pyqgis-win.cmd <../../../scripts/win/set-pyqgis-win.cmd>`_:

.. code-block:: text

    \wtss-qgis> scripts\set_pyqgis_win.cmd


Now your command line python is the same python used in your QGIS plugins. And you are able to install the requirements running `pip` in source code:

.. code-block:: text

    \wtss-qgis> python3 -m pip install -e .[all]


After install the extra requirements, you can use `pb_tool` to compile and deploy the plugin as its follows:

.. code-block:: text

    \wtss-qgis\wtss_plugin> pb_tool compile


To deploy the plugin in Windows, run the script `deploy-win.cmd <../../../scripts/win/deploy-win.cmd>`_, but before set the `USER` variable using your windows user:

.. code-block:: text

    \wtss-qgis\wtss_plugin> set USER=<your_user>


.. code-block:: text

    \wtss-qgis\wtss_plugin> ..\scripts\deploy_win.cmd


To zip generation is only for Linux environemnt, to do so in Windows, you will need to execute some compressing app like `WinRAR <https://www.win-rar.com/start.html?&L=0>`_.

.. note::

    - The final step for all environments is run QGIS and open the **Plugins Manager** and enable the WTSS for **development environment**;
    - To develop in WTSS QGIS Plugin in all operation systems, you will need to install the `QGIS Plugin Reloader <https://plugins.qgis.org/plugins/plugin_reloader/>`_. This plugin will reload any updates after deploys during a QGIS open session, it is useful to test new methods.


=========
Unit Test
=========

Go to the source code folder:

.. code-block:: shell

    $ cd wtss_plugin


Run ``pytest``:

.. code-block:: shell

    $ pytest
