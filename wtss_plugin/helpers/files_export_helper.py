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
import warnings
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn
from PyQt5.QtWidgets import QMessageBox

from ..helpers.pystac_helper import get_source_from_click

warnings.filterwarnings("ignore", category=FutureWarning)

class ApplyTimeSeries:
    """Methods to apply in time series in panda Series format.

    :Methods:
        _set_NaN
        _interpolate
        get_bands_from_df
        apply_to_time_series_df
    """

    def __init__(self):
        """Init the value for band description."""
        self.bands_description = None
        self.selected_band = None

    def _set_NaN(self, value):
        """Set none to missing values of time series."""
        missing_value = self.selected_band.get('nodata')
        if value != missing_value:
            return value
        else:
            return None

    def _interpolate(self, time_series_values):
        """Interpolate the time series using none values in pandas Series."""
        return time_series_values.interpolate(
            method = 'linear',
            limit_direction = 'forward',
            order = 2
        )

    def get_bands_from_df(self, time_series_df: any):
        """Get bands from time series DataFrame."""
        bands = list(time_series_df.keys())
        bands.remove("Index")
        return bands

    def interpolate_df(self, time_series):
        """Apply normalize and interpolation to time series data."""
        for band in self.get_bands_from_df(time_series):
            self.selected_band = self.bands_description.get(band)
            time_series[band] = time_series[band].apply(self._set_NaN)
            time_series[band] = self._interpolate(time_series[band])
        return time_series

class FilesFormat:
    """Files Format Methods.

    :Methods:
        defaultCode
        format_time_series_df
        format_time_series_df_to_json
        get_values_time_series_df
    """

    def defaultCode(self):
        """Return a default python code with blank WTSS parameters."""
        template = (
            Path(os.path.abspath(os.path.dirname(__file__)))
                / 'examples'
                    / 'times_series_export_template.txt'
        )
        return open(template, 'r').read()

    def format_time_series_df(self, time_series, typed: bool = True):
        """Convert time series dict to dataframe to read."""
        timeseries_df = time_series.df()
        timeline = sorted(timeseries_df['datetime'])
        start_date = timeline[0]
        end_date = timeline[len(timeline) - 1]
        cube = time_series.coverage.name
        geom_list = list(set(timeseries_df["geometry"]))
        bands = list(set(timeseries_df["attribute"]))
        time_series_formatted = {
            "sample_id": [],
            "class": [],
            "longitude": [],
            "latitude": [],
            "start_date": [],
            "end_date": [],
            "cube": [],
            "time_series": []
        }
        for row in range(0, len(geom_list)):
            time_series_formatted["sample_id"].append(row + 1)
            time_series_formatted["class"].append("undefined")
            time_series_formatted["longitude"].append(geom_list[row].x)
            time_series_formatted["latitude"].append(geom_list[row].y)
            time_series_formatted["start_date"].append(start_date)
            time_series_formatted["end_date"].append(end_date)
            time_series_formatted["cube"].append(cube)
            grouped_by_geometry = timeseries_df.groupby(['geometry']).get_group(geom_list[row],)
            time_series_ = {}
            time_series_["Index"] = []
            for band in bands:
                grouped_by_band = grouped_by_geometry.groupby("attribute").get_group(band,).reset_index(drop=True).sort_values("datetime")
                if typed:
                    time_series_[band] = grouped_by_band["value"]
                    time_series_["Index"] = grouped_by_band["datetime"]
                else:
                    time_series_[band] = list(grouped_by_band["value"])
                    time_series_["Index"] = [date.strftime('%Y-%m-%d') for date in grouped_by_band["datetime"]]
            time_series_formatted["time_series"].append(time_series_)
        time_series_formatted = pd.DataFrame(time_series_formatted).sort_values("sample_id").reset_index(drop=True)
        return time_series_formatted

    def format_time_series_df_to_json(self, time_series_df):
        """Convert time series dataframe to json to read."""
        time_series_formatted = {'samples': []}
        for index in range(len(time_series_df['sample_id'])):
            time_series_ = time_series_df['time_series'][index]
            for key in time_series_.keys():
                if key != 'Index':
                    time_series_[key] = list(time_series_[key])
                else:
                    time_series_[key] = [date.strftime('%Y-%m-%d') for date in time_series_[key]]
            time_series_formatted['samples'].append({
                "sample_id": int(time_series_df['sample_id'][index]),
                "longitude": float(time_series_df['longitude'][index]),
                "latitude": float(time_series_df['latitude'][index]),
                "cube": time_series_df['cube'][index],
                "time_series": time_series_
            })
        return time_series_formatted

    def get_values_time_series_df(self, time_series_df, line = 0):
        """Get time series dataframe based on line."""
        time_series_formatted = pd.DataFrame(time_series_df['time_series'][line]).sort_values("Index").reset_index(drop=True)
        return time_series_formatted

    def get_aggregations(self, summarize_ts):
        """Get available aggregations for summarize time series."""
        return list(set(summarize_ts.df()['aggregation']))

    def format_summarize_ts(self, summarize_ts, band):
        """Format summarize data to plot in seaborn."""
        result = getattr(summarize_ts, band)
        aggregations = self.get_aggregations(summarize_ts)
        dataframe = {
            "Index": [datetime.strptime(date_, "%Y-%m-%d") for date_ in summarize_ts.timeline]
        }
        for aggregation in aggregations:
            dataframe[aggregation] = getattr(result, aggregation)
        return pd.DataFrame(dataframe)


class FilesExport:
    """Exporting WTSS data in different formats.

    :Methods:
        generateCode
        generateCSV
        generateJSON
    """

    def __init__(self):
        """Set the default values for files format."""
        self.files_format = FilesFormat()
        self.apply_ts = ApplyTimeSeries()

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

    def getExportOptions(self):
        """Set options to export result."""
        return ["CSV", "JSON", "Python", "MatPlotLib"]

    def checkResult(self, time_series):
        """Check if the result is from a geometry."""
        return time_series.query.geom.geometryType() in ['Polygon', 'MultiPoint']

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
            for band in attributes.get("selected_bands"):
                bands_string = bands_string + "'" + str(band) + "', "
            bands_string = bands_string[:len(bands_string)-2] + ")"
            attributes["selected_bands"] = bands_string
            code_to_save = self.files_format.defaultCode().format(**attributes)
            file = open(file_name, "w")
            file.write(code_to_save)
            file.close()
        except FileNotFoundError:
            pass

    def generateJSON(self, file_name, time_series):
        """Generate a JSON file with time series data."""
        try:
            time_series_df = self.files_format.format_time_series_df(time_series)
            data = self.files_format.format_time_series_df_to_json(time_series_df)
            with open(file_name, 'w') as outfile:
                json.dump(data, outfile)
        except FileNotFoundError:
            pass

    def generateCSV(self, file_name, time_series, bands_description):
        """Generate a CSV file with time series data."""
        try:
            self.apply_ts.bands_description = bands_description
            if self.checkResult(time_series):
                time_series_df = self.files_format.format_time_series_df(time_series, typed=False)
                time_series_df.to_csv(file_name, index=False)
            else:
                time_series_df = self.files_format.format_time_series_df(time_series)
                time_series_df = self.files_format.get_values_time_series_df(time_series_df)
                time_series_df = self.apply_ts.interpolate_df(time_series_df)
                time_series_df.to_csv(file_name, index=False)
        except FileNotFoundError:
            pass

    def generateMatPlotFig(self, time_series):
        """Generate using native method to plot for WTSS.py."""
        try:
            time_series.plot()
        except Exception as e:
            self.alert("error", "Error while generate the image!", str(e))

    def generatePlotFig(self, time_series, bands_description):
        """Generate an image .JPEG with time series data in a line chart."""
        try:
            self.apply_ts.bands_description = bands_description
            if self.checkResult(time_series):
                selected_aggregations = ["max", "mean", "min"]
                summarize = time_series.summarize()
                for band_ in time_series.query.attributes:
                    summarize_formatted = self.files_format.format_summarize_ts(summarize, band_)
                    fig = plt.figure(figsize = (12, 5))
                    fig.suptitle(
                        ("Coverage {name} Aggregations for {band}").format(
                            name=str(time_series.coverage.name),
                            band=band_
                        )
                    )
                    seaborn.set_theme(style="darkgrid")
                    for aggregation in selected_aggregations:
                        seaborn.lineplot(
                            data = summarize_formatted,
                            x = "Index", y = aggregation, label = aggregation,
                            markersize = 8, marker = 'o',
                            linestyle = '-', picker = 10
                        )
                    fig.canvas.mpl_connect('pick_event', get_source_from_click)
                    fig.autofmt_xdate()
                    plt.xlabel(None)
                    plt.ylabel(None)
                    plt.legend()
                    plt.show()
            else:
                time_series_df = self.files_format.format_time_series_df(time_series)
                time_series_df = self.files_format.get_values_time_series_df(time_series_df)
                time_series_df = self.apply_ts.interpolate_df(time_series_df)
                fig = plt.figure(figsize = (12, 5))
                fig.suptitle(
                    ("Coverage {name}\n{geom}\nWGS 84 EPSG:4326 ").format(
                        name=str(time_series.coverage.name),
                        geom=str(time_series.query.geom)
                    )
                )
                seaborn.set_theme(style="darkgrid")
                for band in self.apply_ts.get_bands_from_df(time_series_df):
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
            self.alert("error", "Error while generate the image!", str(e))
