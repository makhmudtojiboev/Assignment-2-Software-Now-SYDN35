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
    # Calculating average temperature for each season
    seasonal_avg = data.groupby('SEASON')['TEMPERATURE'].mean().round(1)
    
    # Writing to file
    with open("average_temp.txt", "w") as f:
        for season, temp in seasonal_avg.items():
            f.write(f"{season}: {temp}°C\n")

def find_largest_temp_range(data):
    # Grouping by station and calculate min, max, and range
    station_stats = data.groupby('STATION_NAME')['TEMPERATURE'].agg(['min', 'max'])
    station_stats['range'] = station_stats['max'] - station_stats['min']
    
    # Finding the maximum range
    max_range = station_stats['range'].max()
    
    # Finding all stations with this maximum range
    max_range_stations = station_stats[station_stats['range'] == max_range]
    
    # Writing to file
    with open("largest_temp_range_station.txt", "w") as f:
        for station, row in max_range_stations.iterrows():
            f.write(f"{station}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")

def find_temperature_stability(data):
    # Calculation standard deviation for each station
    station_std = data.groupby('STATION_NAME')['TEMPERATURE'].std()
    
    # Finding min and max standard deviations
    min_std = station_std.min()
    max_std = station_std.max()
    
    # Finding stations with min and max standard deviations
    most_stable = station_std[station_std == min_std]
    most_variable = station_std[station_std == max_std]
    
    # Writing to file
    with open("temperature_stability_stations.txt", "w") as f:
        f.write("Most Stable:\n")
        for station, std in most_stable.items():
            f.write(f"  {station}: StdDev {std:.1f}°C\n")
        
        f.write("Most Variable:\n")
        for station, std in most_variable.items():
            f.write(f"  {station}: StdDev {std:.1f}°C\n")

def main():
    # Creating temperatures folder if it doesn't exist
    if not os.path.exists("temperatures"):
        os.makedirs("temperatures")
        print("Created 'temperatures' folder. Please add your CSV files to this folder and run the program again.")
        return
    
    # Checking if there are any CSV files in the temperatures folder
    csv_files = glob.glob("temperatures/*.csv")
    if not csv_files:
        print("No CSV files found in the 'temperatures' folder. Please add your data files and run the program again.")
        return
    
    # Processing the data
    print("Processing temperature data...")
    data = process_temperature_data()
    
    # Performing analyses
    print("Calculating seasonal averages...")
    calculate_seasonal_averages(data)
    
    print("Finding largest temperature range...")
    find_largest_temp_range(data)
    
    print("Analyzing temperature stability...")
    find_temperature_stability(data)
    
    print("Analysis complete! Results saved to:")
    print("- average_temp.txt")
    print("- largest_temp_range_station.txt")
    print("- temperature_stability_stations.txt")

if __name__ == "__main__":
    main()