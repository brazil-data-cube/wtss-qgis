#
# This file is part of Python QGIS Plugin for WTSS.
# Copyright (C) 2024 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#

"""Python QGIS Plugin for WTSS."""

import datetime

import requests
from pyproj import CRS, Proj, transform
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox
from wtss import *

from .config import Config


class Controls:
    """Sample controls to main class plugin.

    :methods:
        alert
        addItemsTreeView
        formatForQDate
        transformProjection
    """

    def alert(self, type_message, title, text):
        """Show alert message box with a title and info.

        :param title<string>: the message box title.
        :param text<string>: the message box info.
        """
        msg = QMessageBox()
        if type_message == 'error':
            msg.setIcon(QMessageBox.Critical)
        elif type_message == 'warning':
            msg.setIcon(QMessageBox.Warning)
        elif type_message == 'info':
            msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def dialogBox(self, mainDialog, title, text):
        """Create a dialog box to get user info.

        :param mainDialog<string>: the plugin main dialog.
        :param title<string>: the dialog box title.
        :param text<string>: the dialog box info.
        """
        text, okPressed = QInputDialog.getText(mainDialog, title, text, QLineEdit.Normal, "")
        if okPressed and text != "":
            return text
        else:
            return ""

    def addItemsTreeView(self, parent, elements):
        """Create a data struct based on QGIS Tree View.

        :param parent<QStandardItemModel>: the parent node of data struct.
        :param elements<tuple>: list of items in array of tuples.
        """
        for text, children in elements:
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                self.addItemsTreeView(item, children)

    def formatForQDate(self, date_string):
        """Return a QDate format.

        :param date_string<string>: date string with 'yyyy-mm-dd' format.
        """
        return QDate(
            int(date_string[:4]),
            int(date_string[5:-3]),
            int(date_string[8:])
        )

    def transformProjection(self, projection, latitude, longitude):
        """Transform any projection to EPSG:4326.

        :param projection<string>: string format 'EPSG:4326'.
        :param latitude<float>: the point latitude.
        :param longitude<float>: the point longitude.
        """
        lat, lon = transform(
            Proj(init=CRS.from_string(projection)),
            Proj(init=CRS.from_string("EPSG:4326")),
            latitude, longitude
        )
        return {
            "lat": lat,
            "long": lon,
            "crs": "EPSG:4326"
        }

    def formatCoverageDescription(self, description = None):
        """Get description from WTSS Server and format for show.

        :param description<dict>: description object from wtss.
        """
        return "{description}\n\n{spatial}".format(
            description=str(description.get("description")),
            spatial= "*Dimensions*\n\nXmin: {xmin:,.2f}\nXmax: {xmax:,.2f}\nYmin: {ymin:,.2f}\nYmax: {ymax:,.2f}".format(
                xmin=description.get("spatial_extent").get("xmin"),
                xmax=description.get("spatial_extent").get("xmax"),
                ymin=description.get("spatial_extent").get("ymin"),
                ymax=description.get("spatial_extent").get("ymax")
            )
        )

class WTSS_Controls:
    """Class for the service storage rule.

    :Methods:
        setService
        testServiceConnection
        listProducts
        productDescription
        productTimeSeries
    """

    def __init__(self):
        """Build controls for WTSS Servers."""
        self.wtss_host = Config.WTSS_HOST

    def getService(self):
        """Get the service data finding by name."""
        return self.wtss_host

    def setService(self, server_host):
        """Edit the service data finding by name.

        :param server_host<string>: the URL service to edit.
        """
        self.wtss_host = server_host

    def testServiceConnection(self):
        """Check if sevice is available testing connection."""
        try:
            client_wtss = WTSS(Config.WTSS_HOST)
            client_wtss.coverages
            return True
        except:
            return False

    def listProducts(self):
        """Return a dictionary with the list of available products."""
        client_wtss = WTSS(Config.WTSS_HOST)
        return client_wtss.coverages

    def productDescription(self, product):
        """Return a dictionary with product description."""
        client_wtss = WTSS(Config.WTSS_HOST)
        return client_wtss[product]

    def productTimeSeries(self, product, bands, lon, lat, start_date, end_date):
        """Return a dictionary with product time series data.

        :param product<string>: the product name.
        :param bands<tuple>: the selected bands available on product.
        :param lon<float>: the point longitude.
        :param lat<float>: the point latitude.
        :param start_date<string>: start date string with 'yyyy-mm-dd' format.
        :param end_date<string>: end date string with 'yyyy-mm-dd' format.
        """
        if self.testServiceConnection():
            try:
                client_wtss = WTSS(Config.WTSS_HOST)
                time_series = client_wtss[product].ts(
                    attributes=bands,
                    longitude=lon,
                    latitude=lat,
                    start_date=start_date,
                    end_date=end_date
                )
                return time_series
            except:
                return None
        else:
            response = requests.get(
                ("{}/wtss/time_series").format(Config.WTSS_HOST),
                {
                    "coverage": product,
                    "attributes": ",".join(list(bands)),
                    "longitude": lon,
                    "latitude": lat,
                    "start_date": start_date,
                    "end_date": end_date
                },
                timeout=100
            )
            if response.status_code == 200:
                response = response.json()
                tl = response["result"]["timeline"]
                tl = [datetime.strptime(t, "%Y-%m-%d").date() for t in tl]
                response["result"]["timeline"] = tl
                return response
            else:
                return None
