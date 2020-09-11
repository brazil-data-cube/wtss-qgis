#
#   Copyright (C) 2014 National Institute For Space Research (INPE) - Brazil.
#
#  This file is part of Python Client API for Web Time Series Service.
#
#  Web Time Series Service for Python is free software: you can
#  redistribute it and/or modify it under the terms of the
#  GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License,
#  or (at your option) any later version.
#
#  Web Time Series Service for Python is distributed in the hope that
#  it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Web Time Series Service for Python. See LICENSE. If not, write to
#  e-sensing team at <esensing-team@dpi.inpe.br>.
#

import json
from datetime import datetime

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


class wtss:
    """This class implements the WTSS API for Python. See https://github.com/e-sensing/eows for more information on WTSS.

    Example:

        The code snippet below shows how to retrieve a time series for location (latitude = -12, longitude = -54):

            from wtss import wtss

            w = wtss("http://www.dpi.inpe.br/tws")

            ts = w.time_series(coverage = "mod13q1_512", attributes = ["red", "nir"], latitude = -12.0, longitude = -54.0)

            print(ts)

    Attributes:

        host (str): the WTSS server URL.
    """


    def __init__(self, host):
        """Create a WTSS client attached to the given host address (an URL).

        Args:
            host (str): the server URL.
        """
        self.host = host


    def list_coverages(self):
        """Returns the list of all available coverages in the service.

        Returns:
            dict: with a single key/value pair.

            The key named 'coverages' is associated to a list of str:
            { 'coverages' : ['cv1', 'cv2', ..., 'cvn'] }

        """
        return self._request("%s/wtss/list_coverages" % self.host)


    def describe_coverage(self, cv_name):
        """Returns the metadata of a given coverage.

        Args:
            cv_name (str): the coverage name whose schema you are interested in.

        Returns:
            dict: a JSON document with some metadata about the informed coverage.
        """
        result = self._request("%s/wtss/describe_coverage?name=%s" % (self.host, cv_name))
        attrs = dict()
        for attr in result['attributes']:
                attrs[attr['name']] = attr
        result['attributes'] = attrs
        return result


    def time_series(self, coverage, attributes, latitude, longitude, start_date=None, end_date=None):
        """Retrieve the time series for a given location and time interval.

        Args:

            coverage (str): the coverage name whose time series you are interested in.
            attributes(list, tuple, str): the list, tuple or string of attributes you are interested in to have the time series.
            latitude(double): latitude in degrees with the datum WGS84 (EPSG 4326).
            longitude(double): longitude in degrees with the datum WGS84 (EPSG 4326).
            start_date(str, optional): start date.
            end_date(str, optional): end date.

        Raises:
            ValueError: if latitude or longitude is out of range or any mandatory parameter is missing.
            Exception: if the service returns a expcetion
        """

        if not coverage:
            raise ValueError("Missing coverage name.")

        if not attributes:
            raise ValueError("Missing coverage attributes.")

        if type(attributes) in [list, tuple]:
            attributes = ",".join(attributes)
        elif not type(attributes) is str:
            raise ValueError('attributes must be a list, tuple or string')

        if (latitude < -90.0) or (latitude > 90.0):
            raise ValueError('latitude is out-of range!')

        if (longitude < -180.0) or (longitude > 180.0):
            raise ValueError('longitude is out-of range!')

        query_str = "%s/wtss/time_series?coverage=%s&attributes=%s&latitude=%f&longitude=%f" % \
                    (self.host, coverage, attributes, latitude, longitude)

        if start_date:
            query_str += "&start_date={}".format(start_date)

        if end_date:
            query_str += "&end_date={}".format(end_date)

        doc = self._request(query_str)

        if 'exception' in doc:
            raise Exception(doc["exception"])

        tl = doc["result"]["timeline"]

        tl = self._timeline(tl, "%Y-%m-%d")

        doc["result"]["timeline"] = tl

        return time_series(doc)


    def _request(self, uri):

        resource = urlopen(uri)

        doc = resource.read().decode('utf-8')

        return json.loads(doc)


    @classmethod
    def _timeline(cls, tl, fmt):
        """Convert a timeline from a string list to a Python datetime list.

        Args:
            tl (list): a list of strings from a time_series JSON document response.
            fmt (str): the format date (e.g. `"%Y-%m-%d`").

        Returns:
            list (datetime): a timeline with datetime values.
        """
        date_timeline = [datetime.strptime(t, fmt).date() for t in tl]

        return date_timeline


    @classmethod
    def values(cls, doc, attr_name):
        """Returns the time series values for the given attribute from a time_series JSON document response.

        Args:
            doc (dict): a dictionary from a time_series JSON document response.
            attr_name (str): the name of the attribute to retrieve its a time series.

        Returns:
            list: the time series for the given attribute.

        Raises:
            ValueError: if attribute name is not in the document.
        """

        attrs = doc["result"]["attributes"]

        for attr in attrs:
            if attr["attribute"] == attr_name:
                return attr["values"]

        raise ValueError("Time series for attribute '{0}' not found!".format(attr_name))


class time_series:
    """This class is a proxy for the result of a time_series query in WTSS.

    Example:

        The code snippet below shows how to retrieve a time series for location (latitude = -12, longitude = -54):

            from wtss import wtss

            w = wtss("http://www.dpi.inpe.br/tws")

            ts = w.time_series(coverage = "mod13q1_512", attributes = ["red", "nir"], latitude = -12.0, longitude = -54.0)

            print(ts["red"])

            print(ts["nir"])

            print(ts.timeline())


    Attributes:

        attributes (list): the list of attributes from a time_series query to a WTSS server.
        timeline (list): the timeline from a time_series query to a WTSS server.
    """

    def __init__(self, time_series):
        """Initializes a timeseries object from a WTSS time_series query.

        Args:
            time_series (dict): a response from a time_series query to a WTSS server.
        """

        self.doc = time_series

        self.attributes = {}

        for attr in time_series["result"]["attributes"]:
            name = attr["attribute"]
            values = attr["values"]
            self.attributes[name] = values

        self.timeline = time_series["result"]["timeline"]


    def __getitem__(self, item):
        """Returns the list of values for a given attribute.

        Args:
            item (str): the name of an attribute.

        Returns:
            (list): values.
        """
        return self.attributes[item]


    def attributes(self):
        """Returns a list with attribute names.

        Returns:
            (list): a list of strings with the attribute names.
        """

        return self.attributes.keys()
