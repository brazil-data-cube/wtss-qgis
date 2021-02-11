FROM qgis/qgis:release-3_14
COPY . /wtss_qgis
WORKDIR /wtss_qgis
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install testresources \
        && python3 -m pip install --upgrade setuptools \
            && python3 -m pip install -e .[all]
RUN cd wtss_plugin \
    && pb_tool deploy -y --plugin_path /usr/share/qgis/python/plugins