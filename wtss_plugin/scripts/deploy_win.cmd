@echo off
set QGIS_VERSION=3

pb_tool deploy --plugin_path C:\Users\%USER%\AppData\Roaming\QGIS\QGIS%QGIS_VERSION%\profiles\default\python\plugins

cmd.exe
