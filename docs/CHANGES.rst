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


Changes
*******

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
