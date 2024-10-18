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

import os.path
import time
from datetime import datetime
from pathlib import Path

import pystac_client
import qgis.utils
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import (QgsCoordinateReferenceSystem, QgsFeature, QgsPoint,
                       QgsProject, QgsRasterMarkerSymbolLayer, QgsRectangle,
                       QgsSingleSymbolRenderer, QgsSymbol, QgsVectorLayer,
                       QgsWkbTypes)
from qgis.gui import QgsMapToolEmitPoint
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
from qgis.PyQt.QtGui import QIcon, QMovie
from qgis.PyQt.QtWidgets import QAction

from .controller.config import Config
# Import files exporting controls
from .controller.files_export import FilesExport
# Import the STAC args
from .controller.helpers.pystac_helper import stac_args
# Import the controls for the plugin
from .controller.wtss_qgis_controller import Controls, Services
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .wtss_qgis_dialog import wtss_qgisDialog


class wtss_qgis:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Build UI element.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'wtss_qgis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&WTSS')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('wtss_qgis', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = str(Path(Config.BASE_DIR) / 'assets' / 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr(u'WTSS'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Remove the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&WTSS'),
                action)
            self.iface.removeToolBarIcon(action)

    def showHelp(self):
        """Open html doc on default browser."""
        helpfile = (
            Path(os.path.abspath(os.path.dirname(__file__)))
                / 'help' / 'build' / 'html' / 'about.html'
        )
        if os.path.exists(helpfile):
            url = "file://" + str(helpfile)
            self.iface.openURL(url, False)
        qgis.utils.showPluginHelp(packageName="wtss_qgis", filename="index", section="about")

    def initControls(self):
        """Init basic controls to generate files and manage services."""
        self.dlg.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.basic_controls = Controls()
        self.server_controls = Services(user = "application")
        self.files_controls = FilesExport()
        self.enabled_click = False
        self.dlg.enable_canvas_point.setChecked(self.enabled_click)
        self.dlg.enable_canvas_point.stateChanged.connect(self.enableGetLatLng)
        self.dlg.input_longitude.valueChanged.connect(self.checkFilters)
        self.dlg.input_latitude.valueChanged.connect(self.checkFilters)
        self.enableGetLatLng()

    def initLoadingControls(self):
        """Enable loading label."""
        self.movie = QMovie(str(Path(Config.BASE_DIR) / 'assets' / 'loading.gif'))
        self.movie.start()
        self.dlg.loading_label.setStyleSheet("background-color: rgba(216, 216, 216, 0.5)")
        self.dlg.loading_label.setMovie(self.movie)
        self.endLoading()

    def startLoading(self):
        """Start loading label."""
        self.dlg.loading_label.setVisible(True)

    def endLoading(self):
        """End loading label."""
        self.dlg.loading_label.setVisible(False)

    def initIcons(self):
        """Get icons from file system."""
        icon = QIcon(str(Path(Config.BASE_DIR) / 'assets' / 'interrogation-icon.png'))
        self.dlg.show_help_button.setIcon(icon)
        icon = QIcon(str(Path(Config.BASE_DIR) / 'assets' / 'info-icon.png'))
        self.dlg.show_coverage_description.setIcon(icon)
        icon = QIcon(str(Path(Config.BASE_DIR) / 'assets' / 'location-icon.png'))
        self.dlg.search_button.setIcon(icon)
        icon = QIcon(str(Path(Config.BASE_DIR) / 'assets' / 'zoom-icon.png'))
        self.dlg.zoom_selected_point.setIcon(icon)
        self.points_layer_icon_path = str(Path(Config.BASE_DIR) / 'assets' / 'marker-icon.png')

    def initButtons(self):
        """Init the main buttons to manage services and the results."""
        self.dlg.show_help_button.clicked.connect(self.showHelp)
        self.dlg.show_coverage_description.clicked.connect(self.showCoverageDescription)
        self.dlg.save_service.clicked.connect(self.saveService)
        self.dlg.delete_service.clicked.connect(self.deleteService)
        self.dlg.edit_service.clicked.connect(self.editService)
        self.dlg.export_as_python.clicked.connect(self.exportPython)
        self.dlg.export_as_csv.clicked.connect(self.exportCSV)
        self.dlg.export_as_json.clicked.connect(self.exportJSON)
        self.dlg.zoom_selected_point.clicked.connect(self.zoom_to_selected_point)
        self.dlg.zoom_selected_point.setEnabled(False)
        self.dlg.search_button.clicked.connect(self.getTimeSeriesButton)
        self.dlg.search_button.setEnabled(False)

    def initHistory(self):
        """Init and update location history."""
        self.dlg.history_list.clear()
        self.points_layer = None
        self.points_layer_data_provider = None
        self.selected_location = None
        try:
            locations_keys = list(self.locations.keys())
            self.dlg.history_list.addItems(locations_keys)
        except AttributeError:
            self.locations = {}
        self.dlg.history_list.itemClicked.connect(self.getFromHistory)
        self.getLayers()

    def initRasterHistory(self):
        """Add a event listener when a layer is added to check the history of vrt layers."""
        QgsProject.instance().layersAdded.connect(self.updateRasterHistory)

    def initServices(self):
        """Load the registered services based on JSON file."""
        service_names = self.server_controls.getServiceNames()
        if not service_names:
            self.basic_controls.alert("error","502 Error", "The main services are not available!")
        self.dlg.service_selection.addItems(service_names)
        self.dlg.service_selection.activated.connect(self.selectCoverage)
        self.selectCoverage()
        self.data = self.server_controls.loadServices()
        self.model = QStandardItemModel()
        self.basic_controls.addItemsTreeView(self.model, self.data)
        self.dlg.data.setModel(self.model)
        self.dlg.data.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dlg.data.clicked.connect(self.updateDescription)
        self.updateDescription()

    def initRasterPathControls(self):
        """Init raster path location controls."""
        self.enabled_output_path_raster_edit = False
        self.dlg.user_output_path_raster.setText(str(stac_args.get_raster_vrt_folder()))
        self.dlg.user_output_path_raster.setEnabled(self.enabled_output_path_raster_edit)
        self.dlg.change_output_path_raster.clicked.connect(self.updateOutputRasterPath)

    def initRGBoptions(self):
        """Load RGB options with not enabled controls."""
        self.dlg.red_input.setEnabled(False)
        self.dlg.red_input.activated.connect(self.loadRGBOptions)
        self.dlg.green_input.setEnabled(False)
        self.dlg.green_input.activated.connect(self.loadRGBOptions)
        self.dlg.blue_input.setEnabled(False)
        self.dlg.blue_input.activated.connect(self.loadRGBOptions)

    def saveService(self):
        """Save the service based on name and host input."""
        name_to_save = str(self.dlg.service_name.text())
        host_to_save = str(self.dlg.service_host.text())
        try:
            response = self.server_controls.editService(name_to_save, host_to_save)
            if response != None:
                self.selected_service = host_to_save
                self.dlg.service_name.clear()
                self.dlg.service_host.clear()
                self.updateServicesList()
            else:
                self.basic_controls.alert(
                    "error",
                    "(ValueError, AttributeError)",
                    "It is not a valid WTSS Server!"
                )
        except (ValueError, AttributeError, ConnectionRefusedError) as error:
            self.basic_controls.alert("error", "(ValueError, AttributeError)", str(error))

    def updateOutputRasterPath(self):
        """Update the output path for generated rasters."""
        stac_args.update_raster_vrt_folder(self.dlg.user_output_path_raster.text())
        self.enabled_output_path_raster_edit = not self.enabled_output_path_raster_edit
        if self.enabled_output_path_raster_edit:
            self.dlg.change_output_path_raster.setText('Save')
        else:
            self.dlg.change_output_path_raster.setText('Update')
        self.dlg.user_output_path_raster.setEnabled(self.enabled_output_path_raster_edit)
        self.dlg.user_output_path_raster.setText(stac_args.raster_vrt_folder)

    def updateRasterHistory(self):
        """Save a list of generated rasters."""
        self.dlg.virtual_raster_list.clear()
        self.dlg.virtual_raster_list.addItems(stac_args.vrt_history)

    def deleteService(self):
        """Delete the selected active service."""
        try:
            host_to_delete = self.server_controls.findServiceByName(self.metadata_selected.text())
            if host_to_delete == None:
                host_to_delete = self.server_controls.findServiceByName(self.metadata_selected.parent().text())
            self.server_controls.deleteService(host_to_delete.name)
            self.updateServicesList()
        except (ValueError, AttributeError) as error:
            self.basic_controls.alert("error", "(ValueError, AttributeError)", str(error))

    def editService(self):
        """Edit the selected service."""
        try:
            host_to_update = self.server_controls.findServiceByName(self.metadata_selected.text())
            if host_to_update == None:
                host_to_update = self.server_controls.findServiceByName(self.metadata_selected.parent().text())
            self.dlg.service_name.setText(host_to_update.name)
            self.dlg.service_host.setText(host_to_update.host)
        except (ValueError, AttributeError) as error:
            self.basic_controls.alert("error", "(ValueError, AttributeError)", str(error))

    def updateServicesList(self):
        """Update the service list when occurs some change in JSON file."""
        self.data = self.server_controls.loadServices()
        self.model = QStandardItemModel()
        self.basic_controls.addItemsTreeView(self.model, self.data)
        self.dlg.data.setModel(self.model)
        self.dlg.service_selection.clear()
        self.dlg.service_selection.addItems(self.server_controls.getServiceNames())
        self.dlg.service_selection.activated.connect(self.selectCoverage)

    def selectCoverage(self):
        """Fill the blank spaces with coverage metadata for selection."""
        self.dlg.coverage_selection.clear()
        self.dlg.coverage_selection.addItems(
            self.server_controls.listProducts(
                str(self.dlg.service_selection.currentText())
            )
        )
        self.dlg.coverage_selection.activated.connect(self.selectAtributtes)

    def showCoverageDescription(self):
        """Show a information coverage window."""
        if str(self.dlg.coverage_selection.currentText()):
            self.basic_controls.alert(
                "info",
                "Coverage {}".format(str(self.dlg.coverage_selection.currentText())),
                self.basic_controls.getCoverageDescription(
                    self.server_controls,
                    str(self.dlg.service_selection.currentText()),
                    str(self.dlg.coverage_selection.currentText())
                )
            )

    def selectAtributtes(self):
        """Get attributes based on coverage metadata and create the check list."""
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        description = self.server_controls.productDescription(
            str(self.dlg.service_selection.currentText()),
            str(self.dlg.coverage_selection.currentText())
        )
        stac_args.coverage = str(self.dlg.coverage_selection.currentText())
        stac_args.set_channels(
            pystac_client.Client.open(Config.STAC_HOST),
            config = "true_color"
        )
        timeline = description.get("timeline", [])
        timeline = sorted(
            description.get("timeline",[]),
            key = lambda x:
                datetime.strptime(x, '%Y-%m-%d')
        )
        bands = description.get("attributes", {})
        bands = sorted(bands, key = lambda d: d['name'])
        self.bands_checks = {}
        self.dlg.red_input.setEnabled(True)
        self.dlg.green_input.setEnabled(True)
        self.dlg.blue_input.setEnabled(True)
        self.rgb_band_options = {
            'names': [],
            'titles': []
        }
        for band in bands:
            band_name = band.get('name')
            band_common_name = band.get('common_name')
            band_title = f"{str(band_name)} ({str(band_common_name)})"
            band.get('scale_factor', 0)
            self.bands_checks[band_name] = band
            self.bands_checks[band_name]['check'] = QCheckBox(band_title)
            self.bands_checks[band_name]['check'].stateChanged.connect(self.checkFilters)
            self.vbox.addWidget(self.bands_checks.get(band_name).get('check'))
            # Load RGB default options based on selected service to generate vrt rasters.
            self.rgb_band_options['names'].append(band_name)
            self.rgb_band_options['titles'].append(band_title)
        # Load RGB default options to QComboBox for RED Channel
        self.dlg.red_input.clear()
        self.dlg.red_input.addItems(self.rgb_band_options['titles'])
        self.dlg.red_input.setCurrentIndex(self.rgb_band_options['names'].index(stac_args.channels.red))
        # Load RGB default options to QComboBox for GREEN Channel
        self.dlg.green_input.clear()
        self.dlg.green_input.addItems(self.rgb_band_options['titles'])
        self.dlg.green_input.setCurrentIndex(self.rgb_band_options['names'].index(stac_args.channels.green))
        # Load RGB default options to QComboBox for BLUE Channel
        self.dlg.blue_input.clear()
        self.dlg.blue_input.addItems(self.rgb_band_options['titles'])
        self.dlg.blue_input.setCurrentIndex(self.rgb_band_options['names'].index(stac_args.channels.blue))
        # #
        self.widget.setLayout(self.vbox)
        self.dlg.bands_scroll.setWidgetResizable(True)
        self.dlg.bands_scroll.setWidget(self.widget)
        # Update dates for start and end to coverage selection
        self.dlg.start_date.setDate(self.basic_controls.formatForQDate(timeline[0]))
        self.dlg.end_date.setDate(self.basic_controls.formatForQDate(timeline[len(timeline) - 1]))
        self.checkFilters()

    def loadSelectedBands(self):
        """Verify the selected attributes in check list and save in array."""
        selected_attributes = {}
        for band_name in list(self.bands_checks.keys()):
            if self.bands_checks and self.bands_checks.get(band_name).get('check').isChecked():
                selected_attributes[band_name] = self.bands_checks.get(band_name)
        return selected_attributes

    def loadAtributtes(self):
        """Verify the selected attributes in check list and save in array."""
        selected_attributes = [str(band) for band in self.loadSelectedBands().keys()]
        return selected_attributes

    def loadTimeSeries(self):
        """Load time series product data from selected values."""
        try:
            time_series = self.server_controls.productTimeSeries(
                str(self.dlg.service_selection.currentText()),
                str(self.dlg.coverage_selection.currentText()),
                tuple(self.loadAtributtes()),
                float(self.selected_location.get("long")),
                float(self.selected_location.get("lat")),
                str(self.dlg.start_date.date().toString('yyyy-MM-dd')),
                str(self.dlg.end_date.date().toString('yyyy-MM-dd'))
            )
            if time_series == None:
                self.basic_controls.alert("error", "requests.exceptions.HTTPError", "500 Server Error: INTERNAL SERVER ERROR!")
            return time_series
        except:
            return None

    def loadSTACArgs(self, time_series) -> None:
        """Load selected arguments for STAC search."""
        try:
            stac_args.qgis_project = QgsProject.instance()
            stac_args.longitude = time_series.get('query').get('longitude')
            stac_args.latitude = time_series.get('query').get('latitude')
            stac_args.set_timeline(time_series.get('result').get("timeline"))
            self.loadRGBOptions()
        except:
            pass

    def loadRGBOptions(self, time_series) -> None:
        """Load selected arguments for STAC search."""
        try:
            stac_args.channels.red = self.rgb_band_options['names'][self.dlg.red_input.currentIndex()]
            stac_args.channels.green = self.rgb_band_options['names'][self.dlg.green_input.currentIndex()]
            stac_args.channels.blue = self.rgb_band_options['names'][self.dlg.blue_input.currentIndex()]
        except:
            pass

    def exportPython(self):
        """Export python code to file system filling blank spaces with coverage metadata."""
        try:
            name = QFileDialog.getSaveFileName(
                parent=self.dlg,
                caption='Save as python code',
                directory=('{coverage}.{end}.py').format(
                    coverage=str(self.dlg.coverage_selection.currentText()),
                    end=str(self.dlg.end_date.date().toString('yyyy.MM.dd'))
                ),
                filter='*.py'
            )
            attributes = {
                "host": str(self.server_controls.findServiceByName(
                    self.dlg.service_selection.currentText()
                ).host),
                "coverage": str(self.dlg.coverage_selection.currentText()),
                "bands": tuple(self.loadAtributtes()),
                "coordinates": {
                    "crs": self.selected_location.get('crs'),
                    "lat": self.selected_location.get('lat'),
                    "long": self.selected_location.get('long')
                },
                "time_interval": {
                    "start": str(self.dlg.start_date.date().toString('yyyy-MM-dd')),
                    "end": str(self.dlg.end_date.date().toString('yyyy-MM-dd'))
                }
            }
            self.files_controls.generateCode(name[0], attributes)
        except AttributeError as error:
            self.basic_controls.alert("warning", "AttributeError", str(error))

    def exportCSV(self):
        """Export to file system times series data in CSV."""
        try:
            name = QFileDialog.getSaveFileName(
                parent=self.dlg,
                caption='Save as CSV',
                directory=('{coverage}.{end}.csv').format(
                    coverage=str(self.dlg.coverage_selection.currentText()),
                    end=str(self.dlg.end_date.date().toString('yyyy.MM.dd'))
                ),
                filter='*.csv'
            )
            time_series = self.loadTimeSeries()
            self.files_controls.generateCSV(name[0], time_series)
        except AttributeError as error:
            self.basic_controls.alert("warning", "AttributeError", str(error))

    def exportJSON(self):
        """Export the response of WTSS data."""
        try:
            name = QFileDialog.getSaveFileName(
                parent=self.dlg,
                caption='Save as JSON',
                directory=('{coverage}.{end}.json').format(
                    coverage=str(self.dlg.coverage_selection.currentText()),
                    end=str(self.dlg.end_date.date().toString('yyyy.MM.dd'))
                ),
                filter='*.json'
            )
            time_series = self.loadTimeSeries()
            self.files_controls.generateJSON(name[0], time_series)
        except AttributeError as error:
            self.basic_controls.alert("warning", "AttributeError", str(error))

    def plotTimeSeries(self):
        """Generate the plot image with time series data."""
        time_series = self.loadTimeSeries()
        if time_series.get('result', {}).get("timeline", []) != []:
            self.loadSTACArgs(time_series)
            self.files_controls.generatePlotFig(
                time_series = time_series,
                interpolate_data = self.dlg.interpolate_data.isChecked(),
                normalize_data = self.dlg.normalize_data.isChecked(),
                bands_description = self.loadSelectedBands(),
                stac_args=stac_args
            )
        else:
            self.basic_controls.alert("error", "AttributeError", "The times series service returns empty, no data to show!")

    def getLayers(self):
        """Storage the layers in QGIS project."""
        self.layers = QgsProject.instance().layerTreeRoot().children()
        self.layer_names = [layer.name() for layer in self.layers] # Get all layer names
        self.layer = self.iface.activeLayer() # QVectorLayer QRasterFile

    def getFromHistory(self, item):
        """Select location from history storage as selected location."""
        self.selected_location = self.locations.get(item.text(), {})
        self.dlg.input_longitude.setValue(self.selected_location.get('long'))
        self.dlg.input_latitude.setValue(self.selected_location.get('lat'))
        self.draw_point(
            self.selected_location.get('long'),
            self.selected_location.get('lat')
        )

    def getTimeSeriesButton(self):
        """Get time series using canvas click or selected location"""
        self.display_point(None)
        try:
            self.plotTimeSeries()
        except AttributeError:
            pass

    def remove_layer_by_name(self, layer_name):
        """Remove a layer using name."""
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name() == layer_name:
                QgsProject.instance().removeMapLayer(layer.id())

    def zoom_to_point(self, longitude, latitude, scale = None):
        """Zoom in to selected location using longitude and latitude."""
        time.sleep(0.30)
        canvas = self.iface.mapCanvas()
        if not scale:
            scale = 200 * (1 / canvas.scale())
        canvas.setExtent(
            QgsRectangle(
                float(longitude) - scale,
                float(latitude) - scale,
                float(longitude) + scale,
                float(latitude) + scale
            )
        )
        canvas.refresh()

    def zoom_to_selected_point(self):
        """Zoom to selected point."""
        self.zoom_to_point(
            self.selected_location['long'],
            self.selected_location['lat'],
            scale = 0.1
        )

    def draw_point(self, longitude, latitude):
        """Draw the selected points in canvas."""
        points_layer_name = "wtss_coordinates_history"
        points_layer_icon_size = 10

        def add_featute():
            feature = QgsFeature()
            feature.setGeometry(QgsPoint(float(longitude), float(latitude)))
            self.points_layer_data_provider.truncate()
            self.points_layer_data_provider.addFeatures([feature])
            self.points_layer_data_provider.forceReload()

        try:
            add_featute()
        except:
            self.remove_layer_by_name(points_layer_name)
            self.points_layer = QgsVectorLayer(
                "Point?crs=epsg:4326&index=yes",
                points_layer_name, "memory"
            )
            symbol = QgsSymbol.defaultSymbol(QgsWkbTypes.PointGeometry)
            symbol.deleteSymbolLayer(0)
            symbol.appendSymbolLayer(QgsRasterMarkerSymbolLayer(self.points_layer_icon_path))
            symbol.setSize(points_layer_icon_size)
            self.points_layer.setRenderer(QgsSingleSymbolRenderer(symbol))
            self.points_layer.triggerRepaint()
            QgsProject.instance().addMapLayer(self.points_layer)
            self.points_layer_data_provider = self.points_layer.dataProvider()
            add_featute()

    def display_point(self, pointTool):
        """Get the mouse possition and storage as selected location."""
        x = None
        y = None
        if pointTool == None:
            x = self.dlg.input_longitude.value()
            y = self.dlg.input_latitude.value()
        else:
            x = float(pointTool.x())
            y = float(pointTool.y())
            self.dlg.input_longitude.setValue(x)
            self.dlg.input_latitude.setValue(y)
        try:
            self.getLayers()
            self.selected_location = {
                'long' : x,
                'lat' : y,
                'layer_name' : str(self.layer.name()),
                'crs' : str(self.layer.crs().authid())
            }
            history_key = str(
                (
                    "[{long:,.7f}, {lat:,.7f}]"
                ).format(
                    long = self.selected_location.get('long'),
                    lat = self.selected_location.get('lat')
                )
            )
            self.locations[history_key] = self.selected_location
            locations_keys = list(self.locations.keys())
            self.dlg.history_list.clear()
            self.dlg.history_list.addItems(locations_keys)
            self.dlg.history_list.setCurrentRow(len(locations_keys) - 1)
            self.draw_point(x, y)
        except AttributeError:
            pass

    def addCanvasControlPoint(self, enable):
        """Generate a canvas area to get mouse position."""
        crs_id = "4326"
        self.point_tool = None
        self.canvas = None
        if enable:
            self.canvas = self.iface.mapCanvas()
            QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(int(crs_id)))
            self.point_tool = QgsMapToolEmitPoint(self.canvas)
            self.point_tool.canvasClicked.connect(self.display_point)
            self.canvas.setMapTool(self.point_tool)

    def enableGetLatLng(self):
        """Enable get lat lng to search time series."""
        self.enabled_click = self.dlg.enable_canvas_point.isChecked()
        if self.enabled_click:
            self.dlg.input_longitude.setDisabled(True)
            self.dlg.input_latitude.setDisabled(True)
            self.addCanvasControlPoint(True)
        else:
            self.dlg.input_longitude.setDisabled(False)
            self.dlg.input_latitude.setDisabled(False)
            self.addCanvasControlPoint(False)

    def checkFilters(self):
        """Check if lat lng are selected."""
        try:
            if (self.dlg.input_longitude.value() != 0 and self.dlg.input_latitude.value() != 0):
                self.dlg.zoom_selected_point.setEnabled(True)
            else:
                self.dlg.zoom_selected_point.setEnabled(False)
            if (str(self.dlg.coverage_selection.currentText()) != '' and
                    len(self.loadAtributtes()) > 0 and
                        self.dlg.input_longitude.value() != 0 and
                            self.dlg.input_latitude.value() != 0):
                self.dlg.search_button.setEnabled(True)
            else:
                self.dlg.search_button.setEnabled(False)
        except:
            self.dlg.search_button.setEnabled(False)

    def updateDescription(self):
        """Load label on scroll area with product description."""
        try:
            index = self.dlg.data.selectedIndexes()[0]
            self.metadata_selected = index.model().itemFromIndex(index)
            widget = QWidget()
            vbox = QVBoxLayout()
            label = QLabel(
                "{service_metadata}\n\n{coverage_metadata}".format(
                    service_metadata=self.basic_controls.getDescription(
                        name=str(self.metadata_selected.parent().text()),
                        host=str(self.server_controls.findServiceByName(
                            self.metadata_selected.parent().text()
                        ).host),
                        coverage=self.metadata_selected.text()
                    ),
                    coverage_metadata=self.basic_controls.getCoverageDescription(
                        self.server_controls,
                        str(self.metadata_selected.parent().text()),
                        self.metadata_selected.text()
                    )
                )
            )
            label.setWordWrap(True)
            label.heightForWidth(180)
            vbox.addWidget(label)
            widget.setLayout(vbox)
            self.dlg.metadata_scroll_area.setWidgetResizable(True)
            self.dlg.metadata_scroll_area.setWidget(widget)
        except:
            widget = QWidget()
            vbox = QVBoxLayout()
            label = QLabel("Select a coverage!")
            label.setWordWrap(True)
            label.heightForWidth(180)
            vbox.addWidget(label)
            widget.setLayout(vbox)
            self.dlg.metadata_scroll_area.setWidgetResizable(True)
            self.dlg.metadata_scroll_area.setWidget(widget)

    def finish_session(self):
        """Methods to finish when dialog close"""
        #
        # Remove mouse click
        self.addCanvasControlPoint(False)
        #
        # Restore sys.path
        if Config.PYTHONPATH_WTSS_PLUGIN:
            import sys
            sys.path = os.environ['PYTHONPATH_WTSS_PLUGIN'].split(':')
            os.environ.pop('PYTHONPATH_WTSS_PLUGIN')

    def run(self):
        """Run method that performs all the real work."""
        # Init Application
        self.dlg = wtss_qgisDialog()
        # Init Controls
        self.initControls()
        # Services
        self.initServices()
        # Virtual Raster History
        self.initRasterHistory()
        # Output vrt path
        self.initRasterPathControls()
        # RGB Options
        self.initRGBoptions()
        # History
        self.initHistory()
        # Add icons to buttons
        self.initIcons()
        # Start loading label
        self.initLoadingControls()
        # Add functions to buttons
        self.initButtons()
        # show the dialog
        if not self.dlg.isVisible():
            self.dlg.show()
        # Methods to finish session
        self.dlg.finished.connect(self.finish_session)
