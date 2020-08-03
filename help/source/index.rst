.. wtss_qgis documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Python QGIS Plugin for Web Time Series Service
==============================================

.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com/brazil-data-cube/wtss/blob/master/LICENSE
        :alt: Software License

.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle

.. image:: https://badges.gitter.im/brazil-data-cube/community.png
        :target: https://gitter.im/brazil-data-cube/community#
        :alt: Join the chat


About
=====

This is an implementation of the `Web Time Series Service specification <https://github.com/brazil-data-cube/wtss-spec>`_.


**W**\ eb **T**\ ime **S**\ eries **S**\ ervice (WTSS) is a lightweight web service for handling time series data from remote sensing imagery. Given a location and a time interval you can retrieve the according time series as a JSON array of numbers.


In WTSS a coverage is a three dimensional array associate to spatial and temporal reference systems.


WTSS is based on three operations:

- ``list_coverages``: returns the list of all available coverages in the service.

- ``describe_coverage``: returns the metadata of a given coverage.

- ``time_series``: query the database for the list of values for a given location and time interval.


This implementation relies on the `SpatioTemporal Asset Catalog specification <https://github.com/radiantearth/stac-spec>`_. All the the coverages provided by the service are queried in STAC catalogs. Then the GDAL library is used to extract the time series for the specified location.


For more information on WTSS, see:

- `wtss.py <https://github.com/brazil-data-cube/wtss.py>`_: it is a Python client library that supports the communication to a WTSS service.

- `wtss <https://github.com/e-sensing/wtss>`_: it is a client library for R.

- `WTSS Specification <https://github.com/brazil-data-cube/wtss-spec>`_: the WTSS specification using `OpenAPI 3.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md>`_ notation.


Installation
============

See `install.html <./install.html>`_.


License
=======

.. admonition::
    Copyright (C) 2019 INPE.

    Python QGIS Plugin for Web Time Series Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Contents:

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

