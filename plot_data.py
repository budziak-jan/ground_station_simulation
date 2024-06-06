import json
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_locations(location_file, data_file):
    # Load location data
    with open(location_file, 'r') as f:
        locations = json.load(f)
    
    # Load numerical data
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    # Extract city names and numerical values
    cities = [loc['near'] for loc in locations]
    values = [data[city] for city in cities]
    
    # Normalize the numerical values to the range [0, 1] inversely
    normalized_values = [(max(values) - val) / (max(values) - min(values)) for val in values]
    
    # Set up the map
    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-180, 180, -90, 90])  # Adjusted extent to include both poles

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.OCEAN, color='lightblue')
    ax.add_feature(cfeature.LAKES, edgecolor='black', facecolor='lightblue')
    ax.add_feature(cfeature.RIVERS)
    
    # Plot the locations with color-coded markers and scaled dot sizes
    for loc, val, norm_val in zip(locations, values, normalized_values):
        x, y = loc['longitude'], loc['latitude']
        color = (norm_val, 1 - norm_val, 0)  # More green (larger value) to more red (smaller value)
        dot_size = 5 + 5/(norm_val+0.9)  # Adjust dot size based on value
        ax.scatter(x, y, color=color, s=dot_size, label=loc['near'])
        plt.text(x, y, loc['near'], fontsize=8, ha='left', va='bottom', color='black')

    plt.title('Location Plot with Color-coded Markers')
    plt.show()

def main():
    location_file = './cities128_land.json'
    data_file = './city_time.json'
    plot_locations(location_file, data_file)
  
if __name__ == "__main__":
    main()
