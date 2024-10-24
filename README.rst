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

The WTSS Plugin was developed by the Brazil Data Cube project, which offers a straightforward and efficient representation of time series data.

The primary goal of the presented plugin is to streamline and enhance access to the WTSS service by providing users with a graphical interface that integrates directly into the QGIS environment.

This significantly reduces the reliance on command-line inputs, routines, and scripts for retrieving and formatting large datasets of time series, enabling comprehensive analyses of study areas without requiring users to have advanced programming skills.

The following image presents an overview of the plugin:

.. image:: https://github.com/brazil-data-cube/wtss-qgis/tree/master/wtss_plugin/help/source/assets/screenshots/wtss_plugin.png
    :target: https://github.com/brazil-data-cube/wtss-qgis/tree/master/wtss_plugin/help/source/assets/screnshots/wtss_plugin.png
    :width: 100%
    :alt: WTSS-PLUGIN


The plugin WTSS for QGIS is based on the Python programming language with the Python QT library, and its graphical interface with the software QT Designer.

Installation
------------

See `Development Installation <./wtss_plugin/help/source/dev_install.rst>`_.

See `User Installation <./wtss_plugin/help/source/user_install.rst>`_.

Changes
-------

See `History changes <./CHANGES.rst>`_.

References
----------

- VINHAS, L. ; QUEIROZ, G. R. ; FERREIRA, K. R. ; C MARA, G.  Web Services for Big Earth Observation Data. RBC. REVISTA BRASILEIRA DE CARTOGRAFIA (ONLINE), v. 69, p. 6, 2016.

- QUEIROZ, G. R.; FERREIRA, K. R.; VINHAS, L.; CAMARA, G.; COSTA, R. W.; Souza, R. C. M.; Maus,V. W.; Sanchez, A. WTSS: um serviço web para extração de séries temporais de imagens de sensoriamento remoto. In: Proceedings of the XVII Brazilian Symposium on Remote Sensing, pages 7553–7560. 2015.

License
-------

See `LICENSE <./LICENSE>`_.
