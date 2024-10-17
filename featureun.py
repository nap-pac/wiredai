# Libraries
import sqlite3
import pandas as pd
import sys
from pathlib import Path

# Check if executed with filename
if len(sys.argv) < 2:
    print("Error: no File name provided.")
    sys.exit(1)

# Get file name
filename = sys.argv[1]

#Check if file exists
file_path = Path(filename)

if file_path.exists() and file_path.is_file():
    print("Ready to process")
else:
    print(f"Error: '{file_path}' does not exist. Ensure file extension is included")
    sys.exit(1)

# Connect to the SQLite database
conn = sqlite3.connect(file_path)

# Load tables into DataFrames
devices_df = pd.read_sql_query("SELECT * FROM devices", conn)
ssids_df = pd.read_sql_query("SELECT * FROM ssids", conn)
locations_df = pd.read_sql_query("SELECT * FROM locations", conn)

# Close the database connection
conn.close()

# Convert 'first_seen' and 'last_seen' in devices_df to datetime
devices_df['first_seen'] = pd.to_datetime(devices_df['first_seen'], unit='s')
devices_df['last_seen'] = pd.to_datetime(devices_df['last_seen'], unit='s')

# Extract 'hour_of_day' and 'day_of_week' from 'last_seen'
devices_df.insert(5, "hour_of_day", devices_df['last_seen'].dt.hour, True)
devices_df.insert(6, "day_of_week", devices_df['last_seen'].dt.dayofweek, True)

# Convert 'first_seen' and 'last_seen' in ssids_df to datetime
ssids_df['first_seen'] = pd.to_datetime(ssids_df['first_seen'], unit='s')
ssids_df['last_seen'] = pd.to_datetime(ssids_df['last_seen'], unit='s')

# Extract 'hour_of_day' and 'day_of_week' from 'last_seen'
ssids_df.insert(5, "house_of_day", ssids_df['last_seen'].dt.hour, True)
ssids_df.insert(6, "day_of_week", ssids_df['last_seen'].dt.dayofweek, True)

# Process locations_df
locations_df['timestamp'] = pd.to_datetime(locations_df['timestamp'], unit='s')
locations_df.insert(5, "hour_of_dat", locations_df['timestamp'].dt.hour, True)
locations_df.insert(6, "hour_of_dat", locations_df['timestamp'].dt.dayofweek, True)

# Merge DataFrames based on 'mac'
merged_df = pd.merge(devices_df, locations_df, on='mac', how='left')

# Forward fill the missing lat and long
merged_df['lat'] = merged_df['lat'].fillna(method='ffill')
merged_df['lon'] = merged_df['lon'].fillna(method='ffill')

# Remove rows where latitude or longitude is still NaN (if the first entries were NaN)
merged_df = merged_df.dropna(subset=['lat', 'lon'])

# Check the columns of the merged DataFrame
print(merged_df.columns)
# The assumption being that they would have been seen at similar times.
# This is done since the models cannot work with NaN or Null values
# This can't be fixed device side as sometimes the GPS will drop out

# Create the feature DataFrame with available columns
expected_columns = ['mac', 'hour_of_day', 'day_of_week', 'times_seen', 'lat', 'lon']
features_df = merged_df[expected_columns]

# Write the features to a CSV file
features_df.to_csv('test_features3.csv', mode='a', index=False, header=False)

print("Features extracted and written")