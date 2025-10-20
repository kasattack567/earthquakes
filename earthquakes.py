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
    with open('text.json', 'w') as f:
        f.write(text)
    
    with open('text.json', 'r') as f:
        data = json.load(f)

        
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

#Check the structure of the data and the following properties
print(type(data))
print(data.keys())

import numpy as np
import matplotlib.pyplot as plt

# Initialize empty lists to store years and magnitudes
years = []  # This will store the year of each earthquake
magnitudes = []  # This will store the magnitude of each earthquake

# Loop through each earthquake feature in the dataset
for feature in data['features']:
    magnitude = feature['properties']['mag']  # Extract the magnitude of the earthquake
    time_ms = feature['properties']['time']   # Extract the time (in milliseconds since epoch)
    
    # Convert time from milliseconds to seconds
    time_s = time_ms / 1000
    
    # Convert seconds since epoch to year
    # Unix Epoch starts at 1970-01-01 00:00:00 UTC
    # Divide by the number of seconds in a year (365.25 accounts for leap years)
    year = int(1970 + (time_s / (60 * 60 * 24 * 365.25)))  # Convert to year
    
    # Append the year and magnitude to their respective lists
    years.append(year)
    magnitudes.append(magnitude)

# Convert the lists to NumPy arrays for efficient numerical operations
years = np.array(years)
magnitudes = np.array(magnitudes)

# Use numpy.unique to calculate the frequency of earthquakes and average magnitude per year
# np.unique returns the unique years and the count of occurrences for each year
unique_years, counts = np.unique(years, return_counts=True)

# Calculate the average magnitude for each year
# For each unique year, filter the magnitudes array to include only magnitudes for that year
# Then calculate the mean of those magnitudes
average_magnitudes = np.array([magnitudes[years == year].mean() for year in unique_years])

# Print the results for each year
# Loop through the unique years, their counts, and average magnitudes
for year, count, avg_mag in zip(unique_years, counts, average_magnitudes):
    print(f"Year: {year}, Earthquakes: {count}, Average Magnitude: {avg_mag:.2f}")

# Plot the data
fig, ax1 = plt.subplots()  # Create a figure and a set of subplots

# Plot the frequency of earthquakes as a bar chart
ax1.set_xlabel('Year')  # Label for the x-axis
ax1.set_ylabel('Number of Earthquakes', color='tab:blue')  # Label for the left y-axis
ax1.bar(unique_years, counts, color='tab:blue', alpha=0.6, label='Frequency')  # Bar chart for frequency
ax1.tick_params(axis='y', labelcolor='tab:blue')  # Set the color of the left y-axis labels to blue

# Create a second y-axis for the average magnitude
ax2 = ax1.twinx()  # Create a twin y-axis sharing the same x-axis
ax2.set_ylabel('Average Magnitude', color='tab:orange')  # Label for the right y-axis
ax2.plot(unique_years, average_magnitudes, color='tab:orange', marker='o', label='Avg Magnitude')  # Line plot for average magnitude
ax2.tick_params(axis='y', labelcolor='tab:orange')  # Set the color of the right y-axis labels to orange

# Add a title to the plot
plt.title('Earthquake Frequency and Average Magnitude per Year')

# Adjust the layout to prevent overlapping labels
fig.tight_layout()

# Display the plot
plt.show()