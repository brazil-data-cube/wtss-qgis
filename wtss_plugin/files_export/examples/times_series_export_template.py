import matplotlib.pyplot as plt
import numpy as np
from wtss import wtss


# Creating the client with selected service host
client = wtss("{service_host}")

##
# Listing coverages
# Listing the Available Data Products

coverages = client.list_coverages().get("coverages")

print(coverages)

##
# Getting coverage metadata
# Retrieving the Metadata of a Data Product
coverage_metadata = client.describe_coverage("{selected_coverage}")

print(coverage_metadata["attributes"].keys())

timeline = coverage_metadata['timeline']

start = timeline[0]
end = timeline[-1]

print('Interval range: (' + start + ',' + end + ')')

print(coverage_metadata['spatial_extent'])

##
# Time series
# Retrieving the Time Series
bands = {selected_bands}
time_series = client.time_series("{selected_coverage}", bands, {longitude}, {latitude}, "{start_date}", "{end_date}")

# The x-axis will contain the time interval
x = [str(date) for date in time_series.timeline]

plt.title("Coverage {selected_coverage}", fontsize=14)

plt.xlabel("Date", fontsize=10)

plt.ylabel("Value", fontsize=10)

plt.xticks(np.arange(0, len(x), step=float(len(x) // 5)))

plt.grid(b=True, color='gray', linestyle='--', linewidth=0.5)

for band in bands:

    # The y-axis will contain the values in each attribute
    y = time_series.attributes[band]
    plt.plot(x, y, label = band)

plt.legend()
plt.show()

##
#