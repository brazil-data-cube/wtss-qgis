# -*- coding: utf-8 -*-
"""
/***************************************************************************
 wtss_client
                                 A QGIS plugin
 Web Time Series Service (WTSS)
                             -------------------
        begin                : 2020-04-22
        copyright            : (C) 2020 by INPE
        email                : brazildatacube@dpi.inpe.br
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load wtss_client class from file wtss_client.

    :param iface: A QGIS interface instance.
    :type iface: QgisInterface
    """
    #
    from .wtss import wtss_client
    return wtss_client(iface)
