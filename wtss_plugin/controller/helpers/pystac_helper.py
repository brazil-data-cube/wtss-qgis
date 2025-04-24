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

import os
from copy import deepcopy
from pathlib import Path
from typing import List, Optional

import pandas
import pystac_client
from osgeo import gdal
from qgis.core import QgsApplication, QgsRasterLayer

from ..config import Config
from ..wtss_qgis_controller import Controls


class Channels:
    """Set rgb channels values to visualization."""

    def __init__(self, channel = None):
        self.red = ""
        self.green = ""
        self.blue = ""
        if channel != None:
            self.red = channel["red"]
            self.green = channel["green"]
            self.blue = channel["blue"]


class STAC_ARGS:
    """STAC Client Global args."""

    def __init__(self):
        self.qgis_project = None
        self.coverage = ""
        self.longitude = 0
        self.latitude = 0
        self.timeline = []
        self.quick_look = False
        self.channels = Channels()
        self.vrt_history = []
        self.raster_vrt_folder = str(self.get_raster_vrt_folder())

    def get_raster_vrt_folder(self) -> str:
        """Return the location path to save virtual rasters."""
        return QgsApplication.qgisSettingsDirPath()

    def get_point_reference(self) -> any:
        """Return the coordinates as Geojson."""
        return {
            "type": "Point",
            "coordinates": [
                self.longitude,
                self.latitude
            ],
        }

    def update_raster_vrt_folder(self, new_raster_vrt_folder) -> None:
        """Update the location path to save virtual rasters."""
        new_raster_vrt_folder = str(new_raster_vrt_folder)
        last_item = new_raster_vrt_folder[len(new_raster_vrt_folder) - 1]
        if (last_item == "/") or (last_item == "\\"):
            self.raster_vrt_folder = str(new_raster_vrt_folder[0: len(new_raster_vrt_folder) - 1])
        else:
            self.raster_vrt_folder = str(new_raster_vrt_folder)

    def set_timeline(self, timeline: list[str]) -> None:
        """Return a datetime timeline."""
        self.timeline = [pandas.to_datetime(date) for date in timeline]

    def set_channels(self, service, config = "quicklook") -> None:
        collection = service.get_collection(stac_args.coverage)
        rgb = []
        if config == "quicklook":
            rgb = collection.to_dict()["bdc:bands_quicklook"]
        elif config == "true_color":
            rgb = collection.to_dict()['properties']['bdc:visual']['rgb']
        self.channels = Channels({
            "red": rgb[0],
            "green": rgb[1],
            "blue": rgb[2]
        })

    def build_gdal_vrt_raster(self, output_file: str, files: List[str], **options) -> Optional[str]:
        opts = deepcopy(options)
        opts.setdefault("resampleAlg", "nearest")
        opts.setdefault("separate", True)
        vrt_options = gdal.BuildVRTOptions(**opts)
        try:
            gdal.BuildVRT(output_file, files, options = vrt_options)
        except:
            output_file = None
        return output_file


stac_args = STAC_ARGS()

def get_source_from_click(event):
    """Return the source image based on matplotlib event.

    :param event<Event>: The plot event click.
    """
    selected_time = stac_args.timeline[event.ind[0]].strftime('%Y-%m-%d')

    service = pystac_client.Client.open(Config.STAC_HOST)

    item_search = service.search(
        collections = [stac_args.coverage],
        intersects = stac_args.get_point_reference(),
        datetime = selected_time
    )

    items = list(item_search.items())
    item = items[0]

    assets = item.assets

    rgb_href = {}
    channels = stac_args.channels
    for channel in ['red', 'green', 'blue']:
        band = getattr(channels, channel)
        href = assets.get(band).href
        rgb_href[channel] = f'/vsicurl/{href}'

    layer_name = f'{item.id}_{stac_args.channels.red}_{stac_args.channels.green}_{stac_args.channels.blue}'

    vrt_raster_file = str(os.path.join(stac_args.raster_vrt_folder, f'{layer_name}.vrt'))

    vrt_raster_file = stac_args.build_gdal_vrt_raster(
        vrt_raster_file,
        [
            rgb_href['red'],
            rgb_href['green'],
            rgb_href['blue']
        ],
        resampleAlg = 'nearest',
        addAlpha = False,
        separate = True
    )

    if vrt_raster_file:
        layer_names = [
            layer.name()
            for layer in stac_args.qgis_project.mapLayers().values()
        ]
        if layer_name not in layer_names:
            stac_args.vrt_history.append(layer_name)
            stac_args.qgis_project.addMapLayer(
                QgsRasterLayer(vrt_raster_file, layer_name), True
            )
    else:
        controls = Controls()
        controls.alert("error", "Data not found!", "Could not find the request data.")
