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


==========================
Frequently Asked Questions
==========================

The most commom way to check your python environemnt is running `sys.path` in a python compiler in your command line and compare to

.. code-block:: text

    $ git clone h


Requirements, to deploy and publish QGIS Python plugin:


in some cases update your pip


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

