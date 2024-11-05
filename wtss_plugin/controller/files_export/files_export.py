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

import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas
import seaborn

from ..helpers.pystac_helper import get_source_from_click
from ..wtss_qgis_controller import Controls


class FilesExport:
    """Exporting WTSS data in different formats.

    :Methods:
        defaultCode
        to_dataframe
        generateCode
        generateCSV
        generateJSON
    """

    def defaultCode(self):
        """Return a default python code with blank WTSS parameters."""
        template = (
            Path(os.path.abspath(os.path.dirname(__file__)))
                / 'examples'
                    / 'times_series_export_template.txt'
        )
        return open(template, 'r').read()

    def to_dataframe(self, time_series):
        """Convert time series dict to dataframe."""
        time_series_df = pandas.DataFrame({
            "Index": [pandas.to_datetime(date) for date in time_series['result']['timeline']]
        })
        for result in time_series["result"]["attributes"]:
            band = str(result["attribute"])
            time_series_df[band] = result.get("values")
        return time_series_df

    def apply_to_time_series(
            self, time_series_df: any,
            bands_description: any,
            normalize_data: bool,
            interpolate_data: bool
        ):
        """Apply normalize and interpolation to time series data."""
        for band in self.get_bands_from_df(time_series_df):
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
        return time_series_df

    def get_bands_from_df(self, time_series_df: any):
        """Get bands from time series DataFrame."""
        bands = list(time_series_df.keys())
        bands.remove("Index")
        return bands

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
            lat = str(attributes.get("coordinates").get("lat"))
            lon = str(attributes.get("coordinates").get("long"))
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

    def generateJSON(self, file_name, time_series):
        """Generate a JSON file with time series data."""
        try:
            data = time_series
            data.get('result')['timeline'] = [str(date_str) for date_str in time_series.get('result').get("timeline")]
            with open(file_name, 'w') as outfile:
                json.dump(data, outfile)
        except FileNotFoundError:
            pass

    def generateCSV(
            self, file_name, time_series,
            bands_description: any,
            normalize_data: bool,
            interpolate_data: bool
        ):
        """Generate a CSV file with time series data."""
        try:
            time_series_df = self.to_dataframe(time_series)
            time_series_df = self.apply_to_time_series(
                time_series_df, bands_description,
                normalize_data, interpolate_data
            )
            time_series_df.to_csv(file_name, index=False)
        except FileNotFoundError:
            pass

    def generatePlotFig(
            self, time_series,
            bands_description: any,
            normalize_data: bool,
            interpolate_data: bool
        ):
        """Generate an image .JPEG with time series data in a line chart."""
        try:
            time_series_df = self.to_dataframe(time_series)
            time_series_df = self.apply_to_time_series(
                time_series_df, bands_description,
                normalize_data, interpolate_data
            )
            fig = plt.figure(figsize = (12, 5))
            fig.suptitle(
                ("Coverage {name} [{lng:,.7f}, {lat:,.7f}]\nWGS 84 EPSG:4326 ").format(
                    name=str(time_series.get('query').get('coverage')),
                    lng=time_series.get('query').get('longitude'),
                    lat=time_series.get('query').get('latitude')
                )
            )
            seaborn.set_theme(style="darkgrid")
            for band in self.get_bands_from_df(time_series_df):
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
        except Exception as e:
            controls = Controls()
            controls.alert("error", "Error while generate an image!", str(e))
