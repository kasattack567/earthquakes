# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import json
import requests

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    data = response.json()
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates'][0], earthquake['geometry']['coordinates'][1]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    current_max_magnitude = get_magnitude(data["features"][0])
    current_max_location = get_location(data["features"][0])
    for item in data["features"]:
        magnitude = get_magnitude(item)
        # Note: what happens if there are two earthquakes with the same magnitude?
        if magnitude > current_max_magnitude:
            current_max_magnitude = magnitude
            current_max_location = get_location(item)
    return current_max_magnitude, current_max_location

def load_local_data():
    """Load earthquake data from the locally saved text.json file."""
    with open('text.json', 'r') as f:
        data = json.load(f)
    return data

# With all the above functions defined, we can now call them and get the result
data = load_local_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")



import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# --- existing functions above here ---

def get_year(earthquake):
    """Extract the year from the earthquake timestamp."""
    # USGS time is in milliseconds since epoch
    timestamp = earthquake['properties']['time'] / 1000  # convert to seconds
    dt = datetime.utcfromtimestamp(timestamp)
    return dt.year

def analyse_by_year(data):
    """Aggregate number and magnitude of earthquakes by year."""
    counts = defaultdict(int)
    magnitudes_sum = defaultdict(float)

    for quake in data['features']:
        year = get_year(quake)
        mag = get_magnitude(quake)
        if mag is not None:  # just in case there are null magnitudes
            counts[year] += 1
            magnitudes_sum[year] += mag

    # Sort years for plotting
    years = sorted(counts.keys())
    frequencies = [counts[y] for y in years]
    avg_magnitudes = [magnitudes_sum[y] / counts[y] for y in years]

    return years, frequencies, avg_magnitudes

def plot_frequency(years, frequencies):
    plt.figure(figsize=(10, 5))
    plt.bar(years, frequencies, color='steelblue')
    plt.title('Number of Earthquakes per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_average_magnitude(years, avg_magnitudes):
    plt.figure(figsize=(10, 5))
    plt.plot(years, avg_magnitudes, marker='o', color='darkred')
    plt.title('Average Earthquake Magnitude per Year')
    plt.xlabel('Year')
    plt.ylabel('Average Magnitude')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --- run everything ---
if __name__ == "__main__":
    data = get_data()
    print(f"Loaded {count_earthquakes(data)} earthquakes")

    max_magnitude, max_location = get_maximum(data)
    print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")

    years, frequencies, avg_magnitudes = analyse_by_year(data)
    plot_frequency(years, frequencies)
    plot_average_magnitude(years, avg_magnitudes)
