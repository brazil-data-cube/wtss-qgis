..
    This file is part of Python QGIS Plugin for WTSS.
    Copyright (C) 2024 INPE.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.


=======
Changes
=======

Version 1.0.0 (2025-09-12)
--------------------------

- Review the dockerfile to run and test the plugin on different versions of QGIS (#115);
- Update WTSS.py to version 2.0 (#114);
- Create time series analysis for polygon-bounded areas (#113);
- Solved issue "Failed to select coverage - KeyError bdc:visual" (#112);

Version 0.5.0 (2025-04-25)
--------------------------

- Added tile ID reference when creating VRT layer names (`#104 <https://github.com/brazil-data-cube/wtss-qgis/issues/104>`_)
- Removed control to manage WTSS services defining a default host (`#103 <https://github.com/brazil-data-cube/wtss-qgis/issues/103>`_)
- It was improved description of plugin installation using Docker container based on QGIS image (`#102 <https://github.com/brazil-data-cube/wtss-qgis/issues/102>`_)
- Added warning about the Python conda or venv virtual environment to the documentation about installation (`#101 <https://github.com/brazil-data-cube/wtss-qgis/issues/101>`_)
- Added description of errors related to numpy version to documentation about installation (FAQ) (`#100 <https://github.com/brazil-data-cube/wtss-qgis/issues/100>`_)
- Removed imports and methods that are not being used (`#99 <https://github.com/brazil-data-cube/wtss-qgis/issues/99>`_)
- Creating a pipeline to build the package to publish in the official QGIS website (`#91 <https://github.com/brazil-data-cube/wtss-qgis/issues/91>`_)


Version 0.4.0 (2024-11-19)
--------------------------

- Disable file export when there is no selected filters (`#92 <https://github.com/brazil-data-cube/wtss-qgis/issues/92>`_)
- Add rules to normalize and interpolate data to exported data as CSV and JSON files (`#78 <https://github.com/brazil-data-cube/wtss-qgis/issues/78>`_)
- Add menu with advanced options to draw selected points (`#71 <https://github.com/brazil-data-cube/wtss-qgis/issues/71>`_)
- Allow to open multiple images when clicking in the Point (`#73 <https://github.com/brazil-data-cube/wtss-qgis/issues/73>`_)
- Review script template to export as Python code (`#76 <https://github.com/brazil-data-cube/wtss-qgis/issues/76>`_)
- Review the GUI Input to deal with longitude/latitude (`#93 <https://github.com/brazil-data-cube/wtss-qgis/issues/93>`_)
- Remove the GUI option `enable selection``, and keep it always active by default (`#83 <https://github.com/brazil-data-cube/wtss-qgis/issues/83>`_)
- Remove the GUI option `normalize`, and ensure that all time series values are being normalized automatically using "scale factor" (`#84 <https://github.com/brazil-data-cube/wtss-qgis/issues/84>`_)
- Remove the tab to deal with WTSS endpoints (`#85 <https://github.com/brazil-data-cube/wtss-qgis/issues/85>`_)


Version 0.3.1 (2024-10-24)
--------------------------

- Fix numpy version conflicts (`#74 <https://github.com/brazil-data-cube/wtss-qgis/issues/74>`_)
- Add warning and dialog when plot time series crash (`#75 <https://github.com/brazil-data-cube/wtss-qgis/issues/75>`_)
- Update the plugin installation and usage guide in documentation (`#77 <https://github.com/brazil-data-cube/wtss-qgis/issues/77>`_)
- Remove the warning about setting CRS (`#79 <https://github.com/brazil-data-cube/wtss-qgis/issues/79>`_)
- Add single click to set coordinates based on history list (`#80 <https://github.com/brazil-data-cube/wtss-qgis/issues/80>`_)
- Add user data path to save virtual rasters from STAC (`#70 <https://github.com/brazil-data-cube/wtss-qgis/issues/70>`_)
- Manter apenas uma janela do plugin aberta e conectada ao QGIS (`#81 <https://github.com/brazil-data-cube/wtss-qgis/issues/81>`_)
- Garantir a precisão das coordenadas ao selecionar no histórico e ao exportar arquivos (`#82 <https://github.com/brazil-data-cube/wtss-qgis/issues/82>`_)


Version 0.3.0 (2024-10-02)
--------------------------

- Add plot STAC images by clicking (`#72 <https://github.com/brazil-data-cube/wtss-qgis/issues/72>`_)
- Add a check before attempting to retrieve time series (`#63 <https://github.com/brazil-data-cube/wtss-qgis/issues/63>`_)
- Review plot library with `seaborn` (`#53 <https://github.com/brazil-data-cube/wtss-qgis/issues/53>`_)
- Add option or checkbox for user to choose whether to normalize data or not (`#64 <https://github.com/brazil-data-cube/wtss-qgis/issues/64>`_)
- Resolve `nodata` in plot time series with seaborn (`#65 <https://github.com/brazil-data-cube/wtss-qgis/issues/65>`_)
- Resolve coordinates/layers projection in enable canvas points selection (`#66 <https://github.com/brazil-data-cube/wtss-qgis/issues/66>`_)
- Add menu with advanced options to control virtual raster generation (`#67 <https://github.com/brazil-data-cube/wtss-qgis/issues/67>`_)
- Review and update methods for the installation and build steps for plugin (`#68 <https://github.com/brazil-data-cube/wtss-qgis/issues/68>`_)
- Draw and zoom in the points based on selected coordinates to get time series (`#69 <https://github.com/brazil-data-cube/wtss-qgis/issues/69>`_)
- Add user data path to save virtual rasters from STAC (`#70 <https://github.com/brazil-data-cube/wtss-qgis/issues/70>`_)


Version 0.2.0 (2024-08-19)
--------------------------

- Project is active again and under development
- Change License to GPL v3 (`#59 <https://github.com/brazil-data-cube/wtss-qgis/issues/59>`_)
- Review dependencies in package (`#54 <https://github.com/brazil-data-cube/wtss-qgis/issues/54>`_)
- Remove access token dependency (`#51 <https://github.com/brazil-data-cube/wtss-qgis/issues/51>`_)
- Fix mouse click event when search time series (`#52 <https://github.com/brazil-data-cube/wtss-qgis/issues/52>`_)


Version 0.1.0-0 (2020-05-19)
----------------------------

- First version of Plugin with QGIS Version 3+ support
- Add feature to export Python code
- Plot time series using matplotlib
- Initial unittests
- Persist an historic of time series coordinates
