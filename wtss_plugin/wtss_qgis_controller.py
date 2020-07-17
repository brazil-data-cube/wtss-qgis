from pyproj import Proj, transform
from .wtss_client.wtss_client import wtss

from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import QDate

class Controlls:

    def addItemsMenuServices(self, parent, elements):
        for text, children in elements:
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                self.addItemsMenuServices(item, children)

    def formatForQDate(self, date_string):
        # Return a QDate format yyyy-mm-dd
        return QDate(
            int(date_string[:4]),
            int(date_string[5:-3]),
            int(date_string[8:])
        )

    def transformProjection(self, projection, latitude, longitude):
        # transform any projection to EPSG: 4326
        lat, lon = transform(
            Proj(init=projection),
            Proj(init='epsg:4326'),
            latitude, longitude
        )
        return {
            "lat": lat,
            "long": lon,
            "crs": "EPSG: 4326"
        }

    def getDescription(self, name = "Null", host = "Null", coverage = "Null"):
        return (
            "Service name: " + name + "\n" +
            "Host: " + host + "\n" +
            "Active coverage: " + coverage + "\n"
        )

class Services:
    def __init__(self):
        self.services = {
            "Brasil Data Cube": "http://brazildatacube.dpi.inpe.br/",
            "E-sensing": "http://www.esensing.dpi.inpe.br/"
        }
        self.servers = self.loadServices()

    def getServices(self):
        return self.services

    def loadServices(self):
        servers = []
        for server in list(self.getServices().keys()):
            try:
                client_wtss = wtss(self.getServices().get(server))
                coverage_tree = []
                for coverage in client_wtss.list_coverages().get('coverages', []):
                    coverage_tree.append((coverage, []))
                servers.append((server, coverage_tree))
            except RuntimeError:
                services.pop(server)
                pass
        return [("Services", servers)]

    def listProducts(self, service_name):
        client_wtss = wtss(self.services.get(str(service_name)))
        return client_wtss.list_coverages().get("coverages",[])

    def productDescription(self, service_name, product):
        client_wtss = wtss(self.services.get(str(service_name)))
        return client_wtss.describe_coverage(product)

    def productTimeSeries(self, service_name, product, bands, lon, lat, start_date, end_date):
        client_wtss = wtss(self.services.get(str(service_name)))
        return client_wtss.time_series(product, bands, lon, lat, start_date, end_date)

    def addService(self, name, host):
        try:
            client_wtss = wtss(host)
            self.services[name] = host
            return host
        except:
            return None

    def deleteService(self, server_name):
        try:
            return self.services.pop(server_name)
        except:
            return None

    def editService(self, server):
        try:
            service_name = list(server.keys())[0]
            service_host = server.get(service_name)
            service_deleted = self.deleteService(service_name)
            return self.addService(service_name, service_host)
        except:
            return None