..
    This file is part of Python QGIS Plugin for Web Time Series Service.
    Copyright (C) 2020 INPE.

    Python QGIS Plugin for Web Time Series Service is free software;
    You can redistribute it and/or modify it under the terms of the MIT License;


Usage
*****

To use the WTSS extension to satellite image time series it is necessary to generate a user access token in `BDC Auth App <https://brazildatacube.dpi.inpe.br/auth-app>`_.

Enable WTSS-QGIS Plugin
+++++++++++++++++++++++

Open QGIS Desktop and add a vector layer as the figure below:

.. image:: ./assets/screenshots/step1.jpg
    :width: 100%
    :alt: QGIS Desktop

Go to ``Plugins`` tab in ``Management Plugins`` option to verify if WTSS-QGIS is enable. You will find the follow information such a figure below:

.. image:: ./assets/screenshots/step2.jpg
    :width: 100%
    :alt: Enable WTSS-PLUGIN

Run WTSS-QGIS Plugin
++++++++++++++++++++

You can open the WTSS-QGIS Plugin in ``Web`` tab. The following screen will appear:

.. image:: ./assets/screenshots/step3.jpg
    :width: 100%
    :alt: WTSS-PLUGIN

You must select an active ``WTSS server`` that you want to use. And choose the parameters for active ``coverages`` to retrieve the time series information. You must select the available ``bands`` and set a ``start`` and ``end date`` for coverage filter. Finally click on map to get a ``latitude`` and ``longitude`` in vector layer with mouse.

After that, ``Time Series Chart`` will be displayed in new screen with the selected parameters, such a figure:

.. image:: ./assets/screenshots/step4.jpg
    :width: 100%
    :alt: WTSS-PLUGIN