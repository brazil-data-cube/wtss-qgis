import matplotlib.pyplot as plt
import numpy as np
from wtss import WTSS

# Creating the client with selected service host
client = WTSS("http://brazildatacube.dpi.inpe.br/")

##
# Listing coverages
# Listing the Available Data Products

coverages = client.coverages

print(coverages)

##
# Getting coverage metadata
# Retrieving the Metadata of a Data Product
coverage_metadata = client["MOD13Q1-1"]

print(coverage_metadata["attributes"])

timeline = coverage_metadata['timeline']

start = timeline[0]
end = timeline[-1]

print('Interval range: (' + start + ',' + end + ')')

print(coverage_metadata['spatial_extent'])

##
# Time series
# Retrieving the Time Series
bands = ('evi', 'ndvi', 'nir', 'red')
time_series = client["MOD13Q1-1"].ts(
    attributes=bands,
    latitude=-10.21,
    longitude=-56.08,
    start_date="2019-02-18",
    end_date="2019-11-01"
)

# The x-axis will contain the time interval
x = [str(date) for date in time_series.timeline]

plt.title("Coverage MOD13Q1-1", fontsize=14)

plt.xlabel("Date", fontsize=10)

plt.ylabel("Value", fontsize=10)

plt.grid(b=True, color='gray', linestyle='--', linewidth=0.5)

for result in time_series.get("result").get("attributes"):

    # The y-axis will contain the values in each attribute
    y = result.get("values")
    plt.plot(x, y, label = result.get("attribute"))

plt.legend()
plt.show()

##
#