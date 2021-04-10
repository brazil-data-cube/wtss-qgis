FROM qgis/qgis:release-3_16
COPY . /wtss_qgis
WORKDIR /wtss_qgis
RUN pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
        && pip3 install testresources \
            && pip3 install -e .[all]
RUN cd wtss_plugin \
    && pb_tool deploy -y --plugin_path /usr/share/qgis/python/plugins