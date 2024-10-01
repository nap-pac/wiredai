# Libraries
import sqlite3
import pandas as pd

# Connect to the SQLite database
db_path = 'dest_db_2023-09-15_17-07-26.db' # Relative Path
conn = sqlite3.connect(db_path)

# Load tables into DataFrames
devices_df = pd.read_sql_query("SELECT * FROM devices", conn)
ssids_df = pd.read_sql_query("SELECT * FROM ssids", conn)
locations_df = pd.read_sql_query("SELECT * FROM locations", conn)

# Close the database connection
conn.close()

# Convert 'first_seen' and 'last_seen' in devices_df to datetime
devices_df['first_seen'] = pd.to_datetime(devices_df['first_seen'], unit='s')
devices_df['last_seen'] = pd.to_datetime(devices_df['last_seen'], unit='s')

# Display
#print(pd.to_datetime(devices_df['first_seen'], unit='s'))

# Extract 'hour_of_day' and 'day_of_week' from 'last_seen'
devices_df.insert(5, "hour_of_day", devices_df['last_seen'].dt.hour, True)
devices_df.insert(6, "day_of_week", devices_df['last_seen'].dt.dayofweek, True)

# Display
#print(devices_df.head)

# Convert 'first_seen' and 'last_seen' in ssids_df to datetime
ssids_df['first_seen'] = pd.to_datetime(ssids_df['first_seen'], unit='s')
ssids_df['last_seen'] = pd.to_datetime(ssids_df['last_seen'], unit='s')

# Extract 'hour_of_day' and 'day_of_week' from 'last_seen'
ssids_df.insert(5, "house_of_day", ssids_df['last_seen'].dt.hour, True)
ssids_df.insert(6, "day_of_week", ssids_df['last_seen'].dt.dayofweek, True)

# Display
#print(ssids_df.head)

# Process locations_df
locations_df['timestamp'] = pd.to_datetime(locations_df['timestamp'], unit='s')
locations_df.insert(5, "hour_of_dat", locations_df['timestamp'].dt.hour, True)
locations_df.insert(6, "hour_of_dat", locations_df['timestamp'].dt.dayofweek, True)

# Display
#print(locations_df.head)

# Merge DataFrames based on 'mac'
merged_df = pd.merge(devices_df, locations_df, on='mac', how='left')

# Check the columns of the merged DataFrame
print(merged_df.columns)

# Ensure all expected columns are present before selecting features
expected_columns = ['mac', 'hour_of_day', 'day_of_week', 'times_seen']
if 'lat' in merged_df.columns and 'lon' in merged_df.columns: # Not everything has a longitude latitude seen from the kismet data
    expected_columns.extend(['lat', 'lon'])

# Create the feature DataFrame with available columns
features_df = merged_df[expected_columns]

# Write the features to a CSV file
features_df.to_csv('extracted_features_2.csv', index=False)

print("Features extracted and written to extracted_features.csv")
