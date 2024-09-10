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

import csv
import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas
import seaborn

from ..helpers.pystac_helper import STAC_ARGS, get_source_from_click


class FilesExport:
    """Exporting WTSS data in different formats.

    :Methods:
        defaultCode
        generateCode
        generateCSV
        generateJSON
        generatePlotFIG
    """

    def defaultCode(self):
        """Return a default python code with blank WTSS parameters."""
        template = (
            Path(os.path.abspath(os.path.dirname(__file__)))
                / 'examples'
                    / 'times_series_export_template.txt'
        )
        return open(template, 'r').read()

    def generateCode(self, file_name, attributes):
        """Generate a python code file filling WTSS blank spaces.

        :param file_name<str>: file to save path
        :param attributtes<dict>: {
            "host"<str>: the chosen WTSS host
            "coverage"<str>: the name of product to search in WTSS
            "bands"<tuple>: the list of selected bands
            "coordinates"<dict>: {
                "crs"<str>: the projection of Latitude and Longitude of Point
                "lat"<float>: selected Latitude
                "long"<float>: selected Longitude
            }
            "time_interval"<dict>: {
                "start_date"<str>: defining start of time interval in string format <yyyy-MM-dd>
                "end_date"<str>: defining end of time interval in string format <yyyy-MM-dd>
            }
        }
        """
        try:
            bands_string = "("
            for band in attributes.get("bands"):
                bands_string = bands_string + "'" + str(band) + "', "
            bands_string = bands_string[:len(bands_string)-2] + ")"
            lat = "{:,.2f}".format(attributes.get("coordinates").get("lat"))
            lon = "{:,.2f}".format(attributes.get("coordinates").get("long"))
            mapping = {
                "service_host": attributes.get("host"),
                "selected_coverage": attributes.get("coverage"),
                "selected_bands": bands_string,
                "latitude" : lat,
                "longitude" : lon,
                "start_date" : attributes.get("time_interval").get("start"),
                "end_date" : attributes.get("time_interval").get("end")
            }
            code_to_save = self.defaultCode().format(**mapping)
            file = open(file_name, "w")
            file.write(code_to_save)
            file.close()
        except FileNotFoundError:
            pass

    def generateCSV(self, file_name, time_series):
        """Generate a CSV file with time series data.

        :param file_name<str>: file to save path.
        :param time_series<dict>: the time series service reponse dictionary.
        """
        try:
            dates = [str(date_str) for date_str in time_series.get('result').get("timeline")]
            with open(file_name, 'w', newline='') as csvfile:
                fieldnames = ['coverage','latitude','longitude','timeline']
                for result in time_series.get('result').get('attributes'):
                    fieldnames.append(result.get('attribute'))
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
                writer.writeheader()
                ind = 0
                for date in dates:
                    line = {
                        'coverage': time_series.get('query').get('coverage'),
                        'latitude': time_series.get('query').get('latitude'),
                        'longitude': time_series.get('query').get('longitude'),
                        'timeline': date
                    }
                    for result in time_series.get('result').get('attributes'):
                        line[result.get('attribute')] = result.get('values')[ind]
                    ind += 1
                    writer.writerow(line)
        except FileNotFoundError:
            pass

    def generateJSON(self, file_name, time_series):
        """Generate a JSON file with time series data.

        :param file_name<str>: file to save path.
        :param time_series<dict>: the time series service reponse dictionary.
        """
        try:
            data = time_series
            data.get('result')['timeline'] = [str(date_str) for date_str in time_series.get('result').get("timeline")]
            with open(file_name, 'w') as outfile:
                json.dump(data, outfile)
        except FileNotFoundError:
            pass

    def generatePlotFig(
            self, time_series,
            interpolate_data: bool, normalize_data: bool,
            bands_description: any, stac_args: STAC_ARGS
        ):
        """Generate an image .JPEG with time series data in a line chart.

        :param time_series<dict>: the time series service reponse dictionary.
        :param qgis_project_instance<QgsProject>: the qgis project instance.
        """
        try:
            time_series_df = pandas.DataFrame({
                "Index": stac_args.timeline
            })
            fig = plt.figure(figsize = (12, 5))
            fig.suptitle(
                ("Coverage {name} [{lng:,.2f}, {lat:,.2f}] WGS 84 EPSG:4326 ").format(
                    name=str(time_series.get('query').get('coverage')),
                    lng=time_series.get('query').get('longitude'),
                    lat=time_series.get('query').get('latitude')
                )
            )
            seaborn.set_theme(style="darkgrid")
            for result in time_series.get("result").get("attributes"):
                band = str(result.get("attribute"))
                time_series_df[band] = result.get("values")
                if normalize_data:
                    def _normalize(value):
                        if value != bands_description.get(band).get('missing_value'):
                            return value * bands_description.get(band).get('scale_factor')
                        else:
                            return None
                    time_series_df[band] = time_series_df[band].apply(_normalize)
                if interpolate_data:
                    if not normalize_data:
                        def _set_NaN(value):
                            if value != bands_description.get(band).get('missing_value'):
                                return value
                            else:
                                return None
                        time_series_df[band] = time_series_df[band].apply(_set_NaN)
                    time_series_df[band] = time_series_df[band] \
                        .interpolate(
                            method='linear',
                            limit_direction = 'forward',
                            order = 2
                        )
                seaborn.lineplot(
                    data = time_series_df,
                    x = "Index", y = band, label = band,
                    markersize = 8, marker = 'o',
                    linestyle = '-', picker = 10
                )
            fig.canvas.mpl_connect('pick_event', get_source_from_click)
            fig.autofmt_xdate()
            plt.xlabel(None)
            plt.ylabel(None)
            plt.legend()
            plt.show()
        except:
            pass
