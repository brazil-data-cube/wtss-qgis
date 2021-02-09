FROM qgis/qgis:latest
COPY . /wtss_qgis
WORKDIR /wtss_qgis
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade setuptools
RUN python3 -m pip install -e .[all]
RUN cd wtss_plugin && pb_tool deploy -y --plugin_path /usr/share/qgis/python/plugins