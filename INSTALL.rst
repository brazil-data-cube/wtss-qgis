..
    This file is part of Python QGIS Plugin for Web Time Series Service.
    Copyright (C) 2020 INPE.

    Python QGIS Plugin for Web Time Series Service is free software;
    You can redistribute it and/or modify it under the terms of the MIT License;

Installation
************

The Python QGIS Plugin for WTSS depends essentially on:

- `QGIS version +3 <https://qgis.org/en/site/>`_
- `QT Creator version +5 <https://www.qt.io/download>`_
- `Python version +3 <https://www.python.org/>`_

Clone the software repository:

.. code-block:: shell

    $ git clone https://github.com/brazil-data-cube/wtss-qgis

Go to the source code folder:

.. code-block:: shell

    $ cd wtss-qgis

Install requirements `pb_tool <https://pypi.org/project/pb-tool/>`_ to deploy and publish QGIS Python plugin and `pytest <https://pypi.org/project/pytest/>`_ to run unit test with WTSS plugin.

.. code-block:: shell

    $ pip install -e .[all]

Go to the source code folder:

.. code-block:: shell

    $ cd wtss_plugin

Linux
=====

Use ``pb_tool`` to compile and deploy the plugin in Linux OS:

.. code-block:: shell

    $ pb_tool deploy --plugin_path \
        /home/${USER}/.local/share/QGIS/QGIS3/profiles/default/python/plugins

Windows
=======

To deploy the plugin in Windows OS add Python and QGIS Python Scripts to the **PATH** environmental variable such as:

.. code-block:: text

    C:\Users\user\AppData\Local\Programs\Python\Python{version}\Scripts
    C:\Program Files\QGIS {version}\apps\Python37\Scripts

Now you can work from the command line.

On prompt use ``pb_tool`` to compile and deploy WTSS-QGIS plugin:

.. code-block:: text

    > pb_tool deploy --plugin_path \
        C:\Users\user\AppData\Roaming\QGIS\QGIS${version}\profiles\default\python\plugins

Run QGIS and open the Plugin Manager and enable the WTSS-QGIS.

.. note::

    If you want to create a new *Python Virtual Environment* as recommended, please, follow this instruction:

    **1.** Create a new virtual environment linked to Python +3::

        python3 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and install requirements::

        (venv) pip install --upgrade pip

        (venv) pip install -e .[all]
