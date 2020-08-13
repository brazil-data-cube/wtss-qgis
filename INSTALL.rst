..
    This file is part of Python QGIS Plugin for Web Time Series Service.
    Copyright (C) 2019 INPE.

    Python QGIS Plugin for Web Time Series Service is free software;
    You can redistribute it and/or modify it under the terms of the MIT License;


Installation
============

The Python QGIS Plugin for WTSS depends essentially on:

- `QGIS version +3 <https://qgis.org/en/site/>`_
- `QT Creator version +5 <https://www.qt.io/download>`_
- `Python version +3 <https://www.python.org/>`_

Install Requirements
--------------------

Install `pb_tool <https://pypi.org/project/pb-tool/>`_ to deploy and publish QGIS Python plugin and `pytest <https://pypi.org/project/pytest/>`_ to run unit test with WTSS plugin.

.. code-block:: shell

    $ pip install -r requirements.txt

Development Plugin Installation
-------------------------------

Linux Environment
_________________

Clone the software repository:

.. code-block:: shell

    $ git clone https://github.com/brazil-data-cube/wtss-qgis


Go to the source code folder:

.. code-block:: shell

    $ cd wtss-gis

Compile:

.. code-block:: shell

    $ pb_tool compile

Deploy:

.. code-block:: shell

    $ make deploy QGISDIR=<qgis-home>


Windows Environment
___________________

Clone the software repository:

.. code-block:: shell

    $ git clone https://github.com/brazil-data-cube/wtss-qgis
