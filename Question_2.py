# Mohammed Abir Chowdhury - s397008
# Makhmud Tojiboev - s395965

import os
import pandas as pd
import numpy as np
from collections import defaultdict
import glob

def process_temperature_data():
    # Read all CSV files in the temperatures folder
    all_data = []
    
    # Read each file and combine into one DataFrame
    for file_path in glob.glob("temperatures/*.csv"):
        df = pd.read_csv(file_path)
        all_data.append(df)
    
    # Combine all data into a single DataFrame
    combined_data = pd.concat(all_data, ignore_index=True)
    
    # Melt the data to have a long format with month as a separate column
    id_vars = ['STATION_NAME', 'STN_ID', 'LAT', 'LON']
    melted_data = pd.melt(combined_data, id_vars=id_vars, 
                          var_name='MONTH', value_name='TEMPERATURE')
    
    # I am removing rows with missing temperature values
    melted_data = melted_data.dropna(subset=['TEMPERATURE'])
    
    # I am maping the months to seasons (Australian seasons)
    season_map = {
        'December': 'Summer', 'January': 'Summer', 'February': 'Summer',
        'March': 'Autumn', 'April': 'Autumn', 'May': 'Autumn',
        'June': 'Winter', 'July': 'Winter', 'August': 'Winter',
        'September': 'Spring', 'October': 'Spring', 'November': 'Spring'
    }
    
    melted_data['SEASON'] = melted_data['MONTH'].map(season_map)
    
    return melted_data

def calculate_seasonal_averages(data):
    # Calculate average temperature for each season
    seasonal_avg = data.groupby('SEASON')['TEMPERATURE'].mean().round(1)
    
    # Write to file
    with open("average_temp.txt", "w") as f:
        for season, temp in seasonal_avg.items():
            f.write(f"{season}: {temp}°C\n")

def find_largest_temp_range(data):
    # Group by station and calculate min, max, and range
    station_stats = data.groupby('STATION_NAME')['TEMPERATURE'].agg(['min', 'max'])
    station_stats['range'] = station_stats['max'] - station_stats['min']
    
    # Find the maximum range
    max_range = station_stats['range'].max()
    
    # Find all stations with this maximum range
    max_range_stations = station_stats[station_stats['range'] == max_range]
    
    # Write to file
    with open("largest_temp_range_station.txt", "w") as f:
        for station, row in max_range_stations.iterrows():
            f.write(f"{station}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")