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

import urllib
from datetime import datetime

import pandas as pd
import requests
from shapely import to_wkt, wkt
from shapely.geometry import shape
from wtss.timeseries_search import TimeSeriesSearch


class TimeSeriesSearchQGIS(TimeSeriesSearch):

    def make_request(self, host, coverage, params):
        self.params = params
        self.response = requests.post(
            urllib.parse.urljoin(host, f'{coverage}/timeseries'),
            json = self.params,
            headers = {
                'content-type': 'application/json'
            }
        ).json()

    def to_datetime(self, str_):
        return datetime.strptime(str_, '%Y-%m-%d')

    def df(self):
        time_series_response = self.response.get('results')
        dict_template_ts = {
            "attribute": [],
            "geometry": [],
            "value": [],
            "datetime": []
        }
        for result in time_series_response:
            time_series_result = result.get("time_series")
            geometry_str = str(to_wkt(shape(result.get("pixel_center"))))
            timeline = time_series_result.get("timeline")
            values = time_series_result.get("values")
            for band in self.params.get("attributes"):
                dict_template_ts["attribute"] = dict_template_ts["attribute"] + (f"{band}," * len(timeline)).split(",")[:-1]
                dict_template_ts["geometry"] = dict_template_ts["geometry"] + (f"{geometry_str}," * len(timeline)).split(",")[:-1]
                dict_template_ts["datetime"] = dict_template_ts["datetime"] + timeline
                dict_template_ts["value"] = dict_template_ts["value"] + values.get(band)
        df = pd.DataFrame(dict_template_ts)
        df['geometry'] = df['geometry'].apply(wkt.loads)
        df['datetime'] = df['datetime'].apply(self.to_datetime)
        return df
