import os

class PythonFile:
    def __init__(self):
        self.default = os.path.join("files",
            os.path.join("model", "export_as_python.default.py")
        )

    def generateCode(self, attributes):
        bands_string = "( "
        for band in bands:
            bands_string = bands_string + ", " + str(band)
        bands_string = bands_string + ")"
        mapping = {
            "service_host": attributes.get("host"),
            "selected_coverage": attributes.get("coverage"),
            "bands": bands_string,
            "latitude" : attributes.get("coordinates").get("lat"),
            "longitude" : attributes.get("coordinates").get("long"),
            "start_date" : attributes.get("time_interval").get("start"),
            "end_date" : attributes.get("time_interval").get("end")
        }
        code_to_save = open(self.default, 'r').read().format(**mapping)
        return code_to_save