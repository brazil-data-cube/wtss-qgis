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


Development Installation
------------------------

Clone the software repository:

.. code-block:: shell

    $ git clone https://github.com/brazil-data-cube/wtss-qgis


Go to the source code folder:

.. code-block:: shell

    $ cd wtss-gis

Install requirements:

.. code-block:: shell

    $ pip install pb_tool wtss

Compile:

.. code-block:: shell

    $ pb_tool compile

Deploy:

.. code-block:: shell

    $ sudo make deploy QGISDIR=<qgis-home>
