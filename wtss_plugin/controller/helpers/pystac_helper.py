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

import subprocess
from pathlib import Path

import pystac_client
import shapely.geometry
from qgis.core import QgsRasterLayer

from ..config import Config


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
        self.quick_look = False
        self.channels = Channels()

    def get_raster_vrt_folder(self):
        """Return the location path to save virtual rasters."""
        return (Path(Config.BASE_DIR) / 'files_export')

    def set_quick_look(self, service):
        collection = service.get_collection(stac_args.coverage)
        rgb = collection.to_dict().get("bdc:bands_quicklook")
        print(rgb)
        self.channels = Channels({
            "red": rgb[0],
            "green": rgb[1],
            "blue": rgb[2]
        })

stac_args = STAC_ARGS()

def get_source_from_click(event):
    """Return the source image based on matplotlib event.

    :param event<Event>: The plot event click.
    """
    selection_x = event.artist.get_xdata()
    selected_time = str(selection_x[event.ind[0]])

    service = pystac_client.Client.open(Config.STAC_HOST)

    geometry = shapely.geometry.Point(stac_args.longitude, stac_args.latitude)

    item_search = service.search(
        collections = [stac_args.coverage],
        intersects = geometry,
        datetime = selected_time
    )

    items = list(item_search.items())
    item = items[0].assets

    stac_args.set_quick_look(service)

    print(stac_args.channels)

    rgb_href = {}
    channels = stac_args.channels
    for channel in ['red', 'green', 'blue']:
        band = getattr(channels, channel)
        href = item.get(band).href
        rgb_href[channel] = f'/vsicurl/{href}'

    vrt_raster_file = f'{stac_args.get_raster_vrt_folder()}{selected_time}.vrt'
    layer_name = f'{stac_args.coverage}_{selected_time}'

    subprocess.run(
        f'gdalbuildvrt -separate {vrt_raster_file} {rgb_href['red']} {rgb_href['green']} {rgb_href['blue']}',
        shell = True
    )

    stac_args.qgis_project.addMapLayer(
        QgsRasterLayer(vrt_raster_file, layer_name), True
    )
