import numpy as np
import math
import json
from multiprocessing import Pool
from collections import defaultdict


#agregacja danych na potzreby city-time oraz satelite_time
def aggregate_data(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Initialize dictionaries to aggregate time by city name and satellite
    city_time = defaultdict(float)
    satellite_time = defaultdict(float)
    
    # Aggregate time values
    for entry in data:
        city_time[entry["Station"]] += entry["time"]
        satellite_time[entry["satelite"]] += entry["time"]
    
    # Write aggregated data to files
    write_aggregated_data(city_time, "city_time.json")
    write_aggregated_data(satellite_time, "satellite_time.json")

#zapis tych danych do pliku
def write_aggregated_data(aggregated_data, filename):
    # Convert defaultdict to regular dict
    aggregated_data = dict(aggregated_data)
    
    # Write aggregated data to file
    with open(filename, 'w') as file:
        json.dump(aggregated_data, file, indent=4)

#Funkcja oblicza promień "stożka" w jakim jest emitowany sygnał na powierzchnię ziemi
#HPBW - Half Power Beam Width - kąt połowy mocy anteny, kluczony obok wysokości orbity parametr w tym zakresie
def calculate_signal_radius(altitude, HPBW):
    radius = math.tan(math.radians(HPBW/2))*altitude
    return radius

# funkcja oblicza odległośc po powierzchni kuli między dwoma punktami, wiem pewnie troche niedokładnee ale trudno
def haversine_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = np.radians([lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    r = 6371.0

    distance = r * c
    return distance

# obliczenie o ile stopniu przesuniemy się w jeden "tick" zarówno w longitude jak i latitude
def calc_move_speeds(altitude, orbit_period, tps):
    rot_speed = 360/(86164*tps)
    sat_speed = 360/(orbit_period*tps)
    longitude_speed =  rot_speed
    latitude_speed = sat_speed

    return longitude_speed, latitude_speed


def get_cities(filepath):
    file = open(filepath)
    cities = json.load(file)
    return cities

def get_satelites(filepath):
    file = open(filepath)
    satelites = json.load(file)
    return satelites

def get_encounters_json(filepath):
    file = open(filepath)
    encounters = json.load(file)
    return encounters

def get_settings():
    filepath = "settings.json"
    file = open(filepath)
    settings = json.load(file)
    return settings


#Initialization of multi-core calculations
def initialize_calculations(threads):

    settings = get_settings()
    cities = get_cities(settings["cities_file"])

    # encounters = simulate_passes_for_station(cities)
    p = Pool(processes=threads)
    result = p.map(simulate_passes_for_station, cities)
    p.close()
    p.join()
    # Flatten the nested list
    flattened_result = [item for sublist in result for item in sublist]
    print("There were ", len(flattened_result), ' encounters with base stations')
    # Define the filepath

    # Write the flattened result to a JSON file with indentation
    with open(settings["encounters_file"], 'w') as json_file:
        json.dump(flattened_result, json_file, indent=4, separators=(',', ': '))

    aggregate_data(settings["encounters_file"])
    return 0

#Modified function for calculating the encounter time fopr single station
def simulate_passes_for_station(city):
    encounters = []
    settings=get_settings()
    satelites = get_satelites(settings["satelites_file"])
    per_tick_longitude, per_tick_latitude = calc_move_speeds(settings["altitude"], settings["orbit_time"] , tps=settings["tps"])
    signal_radius = calculate_signal_radius(settings["altitude"], settings["HPBW"])

    print(city)

    for satelite in satelites:

        current_longitude = satelite["longitude"]
        current_latitude = satelite["latitude"]

        inside_time = 0
        for tick in range(settings["time"]*settings["tps"]):
            # Update longitude
            current_longitude -= per_tick_longitude
            current_longitude = (current_longitude + 180) % 360 - 180
            # Update latitude
            current_latitude += per_tick_latitude
            current_latitude = (current_latitude + 90) % 180 - 90
            # Calculate distance between two points (for example, Paris and the current location)
            distance_paris = haversine_distance(city["longitude"], city["latitude"], current_longitude, current_latitude)
            if signal_radius > distance_paris:
                inside_time = inside_time +1

        if (inside_time/settings["tps"]) >= settings["min_encounter_time"]:  # Corrected condition
            encounters.append({
                "Station": city["near"],
                "satelite": satelite["sat_no"],
                "time": (inside_time/settings["tps"])
            })

    print("Encounters calculation  for " , city["near"] , " has finished.")
    return encounters




def main():
    initialize_calculations(threads=20)
  
if __name__ == "__main__":
    main()