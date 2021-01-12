..
    This file is part of Python QGIS Plugin for Web Time Series Service.
    Copyright (C) 2020 INPE.

    Python QGIS Plugin for Web Time Series Service is free software;
    You can redistribute it and/or modify it under the terms of the MIT License;
    See LICENSE file for more details.


==============================================
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

.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord

About
=====

This is an implementation of the `Web Time Series Service specification <https://github.com/brazil-data-cube/wtss-spec>`_.

**W**\ eb **T**\ ime **S**\ eries **S**\ ervice (WTSS) is a lightweight web service for handling time series data from remote sensing imagery. Given a location and a time interval you can retrieve the according time series as a JSON array of numbers.

The service called WTSS that has been developed by CGOBT (Coordenação Geral de Observação da Terra)/INPE aims to facilitate access to the satellite image time series (Queiroz et al., 2015; Vinhas et al., 2016).
This service has been used in research projects, such as e-Sensing (FAPESP - grant 2014 / 08398-6), in the Amazon Biome Monitoring Program (PAMZ +) for data validation, in research projects of students from the graduate studies in Applied Computing, Remote Sensing and Earth System Science.

In WTSS a coverage is a three dimensional array associate to spatial and temporal reference systems.

WTSS is based on three operations:

- ``list_coverages``: this operation allows clients to retrieve the capabilities provided by any server that implements WTSS. Or simply put, it returns a list of coverage names available in a server instance. The server response is a JavaScript Object Notation (JSON) document. The names returned by this operation can be used in subsequent operations.

- ``describe_coverage``: this operation returns the metadata for a given coverage identifi ed by its name. It includes its range in the spatial and temporal dimensions;

- ``time_series``: this operation requests the time series of values of a coverage attribute at a given location.

The WTSS performs image recovery using the RasterIO data abstraction library. When a customer submits a request for a time series, the WTSS checks the cache, implemented through REDIS, if the series data is already properly structured and available. If the data is not in the cache, WTSS performs the recovery through the RasterIO library, storing the obtained data in the cache, before sending it to the client. This component was duly reviewed and tested with data from data cubes generated in the BDC project, such as the CBERS-4 cube based on the AWFI sensor.
The acronym REDIS stands for `REmote DIctionary Server (remote dictionary server) <https://redis.io/>`_, as mentioned earlier, this tool was used for the temporary storage of product information identified by the WTSS. This strategy allows an increase in the response speed between one search and another within the application, this service works in conjunction with the application establishing a client and server connection.

This implementation relies on the `SpatioTemporal Asset Catalog specification <https://github.com/radiantearth/stac-spec>`_. All the the coverages provided by the service are queried in STAC catalogs. Then the GDAL library is used to extract the time series for the specified location.

For more information on WTSS, see:

- `wtss.py <https://github.com/brazil-data-cube/wtss.py>`_: it is a Python client library that supports the communication to a WTSS service.

- `wtss <https://github.com/e-sensing/wtss>`_: it is a client library for R.

- `WTSS Specification <https://github.com/brazil-data-cube/wtss-spec>`_: the WTSS specification using `OpenAPI 3.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md>`_ notation.

The following image presents an overview of the plugin:

.. image:: https://github.com/brazil-data-cube/wtss-qgis/blob/master/help/source/assets/img/wtss-qgis.png
        :target: https://github.com/brazil-data-cube/wtss-qgis/blob/master/help/source/assets/img
        :width: 100%
        :alt: WTSS-QGIS

Installation
============

See `INSTALL.rst <./INSTALL.rst>`_.

Unit Tests
==========

See `TESTS.rst <./TESTS.rst>`_.

References
==========

- VINHAS, L. ; QUEIROZ, G. R. ; FERREIRA, K. R. ; C MARA, G.  Web Services for Big Earth Observation Data. RBC. REVISTA BRASILEIRA DE CARTOGRAFIA (ONLINE), v. 69, p. 6, 2016.

- QUEIROZ, G. R.; FERREIRA, K. R.; VINHAS, L.; CAMARA, G.; COSTA, R. W.; Souza, R. C. M.; Maus,V. W.; Sanchez, A. WTSS: um serviço web para extração de séries temporais de imagens de sensoriamento remoto. In: Proceedings of the XVII Brazilian Symposium on Remote Sensing, pages 7553–7560. 2015.

License
=======

.. admonition::
    Copyright (C) 2020 INPE.

    Python QGIS Plugin for Web Time Series Service is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.