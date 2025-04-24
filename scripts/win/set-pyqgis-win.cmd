@REM #
@REM # This file is part of Python QGIS Plugin for WTSS.
@REM # Copyright (C) 2024 INPE.
@REM #
@REM # This program is free software: you can redistribute it and/or modify
@REM # it under the terms of the GNU General Public License as published by
@REM # the Free Software Foundation, either version 3 of the License, or
@REM # (at your option) any later version.
@REM #
@REM # This program is distributed in the hope that it will be useful,
@REM # but WITHOUT ANY WARRANTY; without even the implied warranty of
@REM # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
@REM # GNU General Public License for more details.
@REM #
@REM # You should have received a copy of the GNU General Public License
@REM # along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
@REM #

@echo off
set PYTHON_VERSION=312
set GRASS_VERSION=84
set OSGEO4W_ROOT=C:\OSGeo4W

@echo off
call %OSGEO4W_ROOT%\bin\o4w_env.bat
call %OSGEO4W_ROOT%\apps\grass\grass%GRASS_VERSION%\etc\env.bat

@echo off
path %PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass%GRASS_VERSION%\lib
path %PATH%;%OSGEO4W_ROOT%\apps\Qt5\bin
path %PATH%;%OSGEO4W_ROOT%\apps\Python%PYTHON_VERSION%\Scripts

set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python%PYTHON_VERSION%

set PATH=C:\Program Files\Git\bin;%PATH%

cmd.exe
