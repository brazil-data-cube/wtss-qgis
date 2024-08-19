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
path %PATH%;%OSGEO4W_ROOT%\Python%PYTHON_VERSION%\Scripts

set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python%PYTHON_VERSION%

set PATH=C:\Program Files\Git\bin;%PATH%

cmd.exe
