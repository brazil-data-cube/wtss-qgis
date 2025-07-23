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
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qgis.core import (QgsCoordinateReferenceSystem, QgsFeature, QgsPoint,
                       QgsProject, QgsRasterMarkerSymbolLayer, QgsRectangle,
                       QgsSingleSymbolRenderer, QgsSymbol, QgsVectorLayer,
                       QgsWkbTypes)
from qgis.gui import QgsMapToolEmitPoint, QgsMapToolPan
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
from qgis.PyQt.QtGui import QIcon, QMovie
from qgis.PyQt.QtWidgets import QAction
from shapely import MultiPoint, Point
from shapely.wkt import dumps, loads

from .config import Config
# Import the controls for the plugin
from .controller.wtss_qgis_controller import Controls, WTSS_Controls
# Import files exporting controls
from .helpers.files_export_helper import FilesExport
# Import the STAC args
from .helpers.pystac_helper import stac_args
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .wtss_qgis_dialog import wtss_qgisDialog


class WTSSQgis:
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
                / 'help' / 'build' / 'html' / 'usage.html'
        )
        if os.path.exists(helpfile):
            url = "file://" + str(helpfile)
            self.iface.openURL(url, False)
        qgis.utils.showPluginHelp(packageName="wtss_qgis", filename="index", section="usage")

    def buildMultiPoint(self, featureMultiPoints):
        """Build a MultiPoint Object based on features list of a layer."""
        multipoint_geometry = MultiPoint()
        for feat in featureMultiPoints:
            geoms = loads(feat.geometry().asWkt()).geoms
            for geom in geoms:
                multipoint_geometry = MultiPoint(list(multipoint_geometry.geoms) + [geom])
        return multipoint_geometry

    def getAvailableGeometries(self):
        """Get available layer from tree root."""
        instance_layers = QgsProject.instance().mapLayers().values()
        self.available_geometries = {}
        for layer in instance_layers:
            if isinstance(layer, QgsVectorLayer):
                if  layer.geometryType() == 2:
                    available_items = []
                    for feature in layer.getFeatures():
                        geometry = feature.geometry()
                        if geometry is not None and not geometry.isEmpty():
                            available_items.append({
                                'geometry': loads(geometry.asWkt()).geoms[0],
                                'attributes': dict(zip(layer.fields().names(), feature.attributes()))
                            })
                    self.available_geometries[layer.name()] = available_items
                elif layer.geometryType() == 0 and layer.name() != Config.TEMPORARY_LAYER_NAME:
                    try:
                        geometry = self.buildMultiPoint(layer.getFeatures())
                        self.available_geometries[layer.name()] = [{
                            'geometry': geometry,
                            'attributes': {'type': 'MultiPoint Geometry'}
                        }]
                    except:
                        pass
        self.dlg.available_layers.clear()
        available_layers_ = list(self.available_geometries.keys())
        self.dlg.available_layers.addItems(available_layers_)
        self.dlg.available_layers.setCurrentIndex(0)
        self.dlg.available_layers.activated.connect(self.getGeometriesFromSelectLayer)
        if len(available_layers_) > 0:
            self.getGeometriesFromSelectLayer()

    def initControls(self):
        """Init basic controls to generate files and manage services."""
        self.dlg.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.dlg.setFixedSize(self.dlg.size().width(), self.dlg.size().height())
        self.basic_controls = Controls()
        self.wtss_controls = WTSS_Controls()
        self.files_controls = FilesExport()
        self.enabled_click = True
        self.addCanvasControlPoint(self.enabled_click)
        self.dlg.location_tabs.currentChanged.connect(self.changeGeometryType)
        self.dlg.input_longitude.valueChanged.connect(self.checkFilters)
        self.dlg.input_latitude.valueChanged.connect(self.checkFilters)
        self.listCoverages()
        self.getAvailableGeometries()
        self.changeGeometryType(0)

    def wtss_connection_ok(self):
        try:
            _ = requests.get(Config.WTSS_HOST)
            return True
        except requests.ConnectionError as e:
            controls = Controls()
            controls.alert(
                "error",
                "WTSS Connection Error!", str(e)
            )
            return False

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
        icon = QIcon(str(Path(Config.BASE_DIR) / 'assets' / 'refresh-icon.png'))
        self.dlg.refresh_layers.setIcon(icon)
        icon = QIcon(str(Path(Config.BASE_DIR) / 'assets' / 'refresh-icon.png'))
        self.dlg.refresh_wkt.setIcon(icon)
        icon = QIcon(str(Path(Config.BASE_DIR) / 'assets' / 'save-icon.png'))
        self.dlg.export_result.setIcon(icon)
        self.points_layer_icon_path = str(Path(Config.BASE_DIR) / 'assets' / 'marker-icon.png')

    def initButtons(self):
        """Init the main buttons to manage services and the results."""
        self.dlg.show_help_button.clicked.connect(self.showHelp)
        self.dlg.show_coverage_description.clicked.connect(self.showCoverageDescription)
        self.dlg.export_result.clicked.connect(self.exportAsType)
        self.dlg.zoom_selected_point.clicked.connect(self.zoom_to_selected_point)
        self.dlg.zoom_selected_point.setEnabled(True)
        self.dlg.refresh_layers.clicked.connect(self.getAvailableGeometries)
        self.dlg.refresh_wkt.clicked.connect(self.validateWKT)
        self.dlg.search_button.clicked.connect(self.getTimeSeriesButton)
        self.dlg.search_button.setEnabled(False)
        self.initExportOptions()
        self.enabledSearchButtons(False)

    def initExportOptions(self):
        """Init the combo box select option to export"""
        self.dlg.export_result_as_type.addItems(self.files_controls.getExportOptions())

    def initHistory(self):
        """Init and update location history."""
        self.dlg.history_list.clear()
        self.points_layer = None
        self.points_layer_data_provider = None
        self.selected_geometry = None
        try:
            self.dlg.history_list.addItems(list(self.locations.keys()))
        except AttributeError:
            self.locations = {}
        self.dlg.history_list.itemClicked.connect(self.getFromHistory)
        self.getLayers()

    def initRasterHistory(self):
        """Add a event listener when a layer is added to check the history of vrt layers."""
        QgsProject.instance().layersAdded.connect(self.updateRasterHistory)

    def initRasterPathControls(self):
        """Init raster path location controls."""
        self.dlg.user_output_path_raster.setEnabled(False)
        self.dlg.user_output_path_raster.setText(stac_args.raster_vrt_folder)
        self.dlg.change_output_path_raster.clicked.connect(self.updateOutputRasterPath)

    def initRGBoptions(self):
        """Load RGB options with not enabled controls."""
        self.dlg.red_input.setEnabled(False)
        self.dlg.red_input.activated.connect(self.loadRGBOptions)
        self.dlg.green_input.setEnabled(False)
        self.dlg.green_input.activated.connect(self.loadRGBOptions)
        self.dlg.blue_input.setEnabled(False)
        self.dlg.blue_input.activated.connect(self.loadRGBOptions)

    def setCRS(self):
        """Set the CRS in project instance."""
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem(int("4326")))

    def updateOutputRasterPath(self):
        """Update the output path for generated rasters."""
        qturl_request = QFileDialog.getExistingDirectoryUrl(
            parent=self.dlg,
            caption='Select a path to save virtual raster files'
        )
        stac_args.update_raster_vrt_folder(str(qturl_request.path()))
        self.dlg.user_output_path_raster.setText(stac_args.raster_vrt_folder)

    def updateRasterHistory(self):
        """Save a list of generated rasters."""
        self.dlg.virtual_raster_list.clear()
        self.dlg.virtual_raster_list.addItems(stac_args.vrt_history)

    def listCoverages(self):
        """Fill the blank spaces with coverage metadata for selection."""
        products = self.wtss_controls.listProducts()
        self.dlg.coverage_selection.clear()
        self.dlg.coverage_selection.addItems(products)
        self.dlg.coverage_selection.setCurrentIndex(0)
        self.dlg.coverage_selection.activated.connect(self.selectAtributtes)
        self.selectAtributtes()

    def showCoverageDescription(self):
        """Show a information coverage window."""
        selected_coverage = str(self.dlg.coverage_selection.currentText())
        if selected_coverage:
            self.basic_controls.alert(
                "info",
                "Coverage {}".format(selected_coverage),
                self.basic_controls.formatCoverageDescription(
                    self.wtss_controls.productDescription(selected_coverage)
                )
            )

    def selectAtributtes(self):
        """Get attributes based on coverage metadata and create the check list."""
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        description = self.wtss_controls.productDescription(
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
        bands = description.attributes
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

    def changeGeometryType(self, index):
        """When geometry selection tab changed."""
        self.selected_geometry = None
        if index == 0:
            # 0 => Longitude / Latitude tab selected
            self.wkt_string = False
            self.geom_search = False
            self.addCanvasControlPoint(True)
            self.dlg.input_longitude.setValue(0)
            self.dlg.input_latitude.setValue(0)
        elif index == 1:
            # 0 => Geometry tab selected
            self.getAvailableGeometries()
            if len(list(self.available_geometries.keys())) > 0:
                self.wkt_string = False
                self.geom_search = True
                self.addCanvasControlPoint(False)
            else:
                self.basic_controls.alert("warning", "Warning!", "No geometry to select!")
                self.dlg.location_tabs.setCurrentIndex(0)
                self.changeGeometryType(0)
        elif index == 2:
            self.dlg.selected_wkt.setText('')
            self.dlg.selected_wkt.setPlaceholderText("WKT String...")
            self.wkt_string = True
            self.geom_search = False
            self.addCanvasControlPoint(False)
        self.checkFilters()

    def getGeometriesFromSelectLayer(self):
        """Get available polygons from selected layers."""
        selected_layer_items = self.available_geometries[self.dlg.available_layers.currentText()]
        self.available_items_from_layer = {}
        for item in selected_layer_items:
            key = f'{self.dlg.available_layers.currentText()}: ('
            for attr in item['attributes']:
                value = str(item["attributes"][attr])
                value = (value[:30] + '...') if (len(value) > 30) else value
                key += f'{attr}:{value},'
            key += ")"
            self.available_items_from_layer[key] = item['geometry']
        self.dlg.available_geometries.clear()
        self.dlg.available_geometries.addItems(list(self.available_items_from_layer.keys()))
        self.dlg.available_geometries.setCurrentIndex(0)
        self.dlg.available_geometries.activated.connect(self.selectGeometry)
        self.selectGeometry()

    def selectGeometry(self):
        """Select geometry from selected layer."""
        self.selected_geometry = self.available_items_from_layer[self.dlg.available_geometries.currentText()]
        self.checkFilters()

    def validateWKT(self):
        """Check if has a WKT string."""
        try:
            self.selected_geometry = loads(str(self.dlg.selected_wkt.text()))
            if self.selected_geometry.geometryType() not in ['Polygon', 'MultiPoint']:
                raise("Geometry not accepted")
            self.checkFilters()
        except Exception as e:
            self.basic_controls.alert("error", "Error reading WKT string!", str(e))

    def loadTimeSeries(self):
        """Load time series product data from selected values."""
        try:
            time_series = self.wtss_controls.productTimeSeries(
                str(self.dlg.coverage_selection.currentText()),
                list(self.loadAtributtes()),
                str(self.dlg.start_date.date().toString('yyyy-MM-dd')),
                str(self.dlg.end_date.date().toString('yyyy-MM-dd')),
                geometry = self.selected_geometry
            )
            if time_series == None:
                self.basic_controls.alert("error", "requests.exceptions.HTTPError", "500 Server Error: INTERNAL SERVER ERROR!")
            else:
                self.save_on_history()
            return time_series
        except:
            return None

    def loadSTACArgs(self, time_series) -> None:
        """Load selected arguments for STAC search."""
        try:
            stac_args.qgis_project = QgsProject.instance()
            stac_args.geometry = self.selected_geometry
            stac_args.set_timeline(time_series)
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
            if name[0] != '':
                time_series = self.loadTimeSeries()
                if time_series.total_locations() > 0:
                    self.files_controls.generateCSV(name[0], time_series, bands_description = self.loadSelectedBands())
                else:
                    self.basic_controls.alert("warning", "Warning", "The times series service returns empty, no data to show!")
        except AttributeError as error:
            self.basic_controls.alert("error", "AttributeError", str(error))

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
            if name[0] != '':
                time_series = self.loadTimeSeries()
                if time_series.total_locations() > 0:
                    self.files_controls.generateJSON(name[0], time_series)
                else:
                    self.basic_controls.alert("warning", "Warning", "The times series service returns empty, no data to show!")
        except AttributeError as error:
            self.basic_controls.alert("error", "AttributeError", str(error))

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
                "service_host": str(self.wtss_controls.getService()),
                "selected_coverage": str(self.dlg.coverage_selection.currentText()),
                "selected_bands": tuple(self.loadAtributtes()),
                "geometry": str(self.selected_geometry.wkt),
                "start_date": str(self.dlg.start_date.date().toString('yyyy-MM-dd')),
                "end_date": str(self.dlg.end_date.date().toString('yyyy-MM-dd'))
            }
            self.files_controls.generateCode(name[0], attributes)
        except AttributeError as error:
            self.basic_controls.alert("warning", "AttributeError", str(error))

    def plotMatLib(self):
        """Generate the plot image using native method for WTSS.py."""
        try:
            time_series = self.loadTimeSeries()
            if time_series.total_locations() > 0:
                self.files_controls.generateMatPlotFig(time_series)
        except:
            self.basic_controls.alert("error", "AttributeError", "The times series service returns empty, no data to show!")

    def plotTimeSeries(self):
        """Generate the plot image with time series data."""
        time_series = self.loadTimeSeries()
        if time_series.total_locations() > 0:
            self.loadSTACArgs(time_series)
            self.files_controls.generatePlotFig(time_series, bands_description = self.loadSelectedBands())
        else:
            self.basic_controls.alert("error", "AttributeError", "The times series service returns empty, no data to show!")

    def exportAsType(self):
        """Export result based on combo box selection."""
        ext = self.dlg.export_result_as_type.currentText()
        if ext == "CSV":
            self.exportCSV()
        elif ext == "JSON":
            self.exportJSON()
        elif ext == "Python":
            self.exportPython()
        elif ext == "MatPlotLib":
            self.plotMatLib()

    def getLayers(self):
        """Storage the layers in QGIS project."""
        self.layers = QgsProject.instance().layerTreeRoot().children()
        self.layer_names = [layer.name() for layer in self.layers] # Get all layer names
        self.layer = self.iface.activeLayer() # QVectorLayer QRasterFile

    def getFromHistory(self, item):
        """Select location from history storage as selected location."""
        selection = self.locations.get(item.text(), None)
        if selection.geometryType() == "Point":
            self.dlg.location_tabs.setCurrentIndex(0)
            self.changeGeometryType(0)
            self.selected_geometry = selection
            if self.selected_geometry.geometryType() == 'Point':
                self.dlg.input_longitude.setValue(self.selected_geometry.x)
                self.dlg.input_latitude.setValue(self.selected_geometry.y)
                self.draw_point(
                    self.selected_geometry.x,
                    self.selected_geometry.y
                )
        else:
            self.dlg.location_tabs.setCurrentIndex(2)
            self.changeGeometryType(2)
            self.selected_geometry = selection
            self.dlg.selected_wkt.setText(self.selected_geometry.wkt)
            self.validateWKT()
            self.geom_search = True

    def getTimeSeriesButton(self):
        """Get time series using canvas click or selected location"""
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
        self.addCanvasControlPoint(self.enabled_click)
        if (self.dlg.input_longitude.value() != 0 and self.dlg.input_latitude.value() != 0):
            self.dlg.zoom_selected_point.setEnabled(True)
            self.draw_point(self.dlg.input_longitude.value(), self.dlg.input_latitude.value())
            self.zoom_to_point(
                self.dlg.input_longitude.value(),
                self.dlg.input_latitude.value(),
                scale = 0.1
            )

    def set_draw_point(self, longitude, latitude):
        """Create featur to draw temporary point in canvas."""
        feature = QgsFeature()
        feature.setGeometry(QgsPoint(float(longitude), float(latitude)))
        self.points_layer_data_provider.truncate()
        self.points_layer_data_provider.addFeatures([feature])
        self.points_layer_data_provider.forceReload()

    def draw_point(self, longitude, latitude):
        """Draw the selected points in canvas."""
        self.getLayers()
        if len(self.layers) > 0:
            self.setCRS()
            points_layer_name = Config.TEMPORARY_LAYER_NAME
            points_layer_icon_size = 10
            try:
                self.set_draw_point(longitude, latitude)
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
                self.set_draw_point(longitude, latitude)

    def save_on_history(self):
        """Get lng/lat coordinates and save on history list."""
        self.locations[self.selected_geometry.wkt] = self.selected_geometry
        locations_keys = list(self.locations.keys())
        self.dlg.history_list.clear()
        self.dlg.history_list.addItems(locations_keys)
        self.dlg.history_list.setCurrentRow(len(locations_keys) - 1)

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
            self.selected_geometry = Point(x, y)
            self.draw_point(x, y)
        except AttributeError:
            pass

    def addCanvasControlPoint(self, enable):
        """Generate a canvas area to get mouse position."""
        self.point_tool = None
        self.pan_map = None
        self.canvas = self.iface.mapCanvas()
        if enable:
            self.setCRS()
            self.point_tool = QgsMapToolEmitPoint(self.canvas)
            self.point_tool.canvasClicked.connect(self.display_point)
            self.canvas.setMapTool(self.point_tool)
        else:
            self.pan_map = QgsMapToolPan(self.canvas)
            self.canvas.setMapTool(self.pan_map)

    def enabledSearchButtons(self, enable):
        """Enable the buttons to load time series."""
        self.dlg.search_button.setEnabled(enable)
        self.dlg.export_result_as_type.setEnabled(enable)
        self.dlg.export_result.setEnabled(enable)

    def checkFilters(self):
        """Check if lat lng are selected."""
        try:
            if (str(self.dlg.coverage_selection.currentText()) != '' and len(self.loadAtributtes()) > 0):
                if self.geom_search:
                    if (str(self.dlg.available_layers.currentText()) != '' and str(self.dlg.available_geometries.currentText()) != ''):
                        self.enabledSearchButtons(True)
                    else:
                        self.enabledSearchButtons(False)
                elif self.wkt_string:
                    if self.selected_geometry != None:
                        self.enabledSearchButtons(True)
                    else:
                        self.enabledSearchButtons(False)
                else:
                    if (self.dlg.input_longitude.value() != 0 and self.dlg.input_latitude.value() != 0):
                        self.enabledSearchButtons(True)
                    else:
                        self.enabledSearchButtons(False)
            else:
                self.enabledSearchButtons(False)
        except:
            self.enabledSearchButtons(False)

    def finish_session(self):
        """Methods to finish when dialog close"""
        #
        # Remove mouse click
        self.addCanvasControlPoint(False)
        #
        # Restore sys.path
        if Config.PYTHONPATH_WTSS_PLUGIN:
            try:
                import sys
                sys.path = os.environ['PYTHONPATH_WTSS_PLUGIN'].split(':')
                os.environ.pop('PYTHONPATH_WTSS_PLUGIN')
            except:
                pass

    def dialogShow(self):
        """Rules to start dialog."""
        wtss_qgis = qgis.utils.plugins.get("wtss_plugin", None)
        if wtss_qgis:
            wtss_qgis.dlg.show()
        else:
            self.dlg.show()

    def run(self):
        """Run method that performs all the real work."""
        try:
            # Init Application
            self.dlg = wtss_qgisDialog()
            if self.wtss_connection_ok():
                # Init Controls
                self.initControls()
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
                self.dialogShow()
                # Methods to finish session
                self.dlg.finished.connect(self.finish_session)
        except Exception as e:
            # Exception raises error message and closes dialog
            controls = Controls()
            controls.alert("error", "Error while starting plugin!", str(e))
            self.dlg.close()
