# Libraries
import sqlite3
import pandas as pd
import re
import numpy as np

def valid_mac_adddress(macList):
    # Regex pattern for valid MAC
    macRegex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

    validMacs = []

    for mac in macList:
        if macRegex.match(mac):
            validMacs.append(mac)
        else:
            print(f"Invalid MAC address: {mac}")
    
    return validMacs


def main():
    # Connect to the SQLite database
    dbPath = 'Kismet-20240819-06-29-51-1.kismet' # Relative Path, also .kismet files are just sqlite files
    # don't forget to add .kismet end otherwise it won't open
    conn = sqlite3.connect(dbPath)

    # Load the tables
    devicesDf = pd.read_sql_query("SELECT * FROM devices", conn) # Device Data
    packetsDf = pd.read_sql_query("SELECT * FROM packets", conn) # Wi-Fi devices Raw Data
    dataDf = pd.read_sql_query('SELECT * FROM data', conn) # Bluetooth device Raw Data

    # Close the database connection
    conn.close()

    #Extract the data
    extDevRows = devicesDf.loc[:, ['devmac', 'first_time', 'last_time']]
    # We use this table to find  
    # MAC | First seen | Last seen
    # First and Last seen are need to find the period of time it was seen
 
    extPackRows = packetsDf.loc[:, ['sourcemac', 'ts_sec', 'lat', 'lon', 'signal']]
    # Main table for Wi-Fi where we find: 
    # What | When | LAT | LON | signal strengh
    extPackRows.rename(columns={'sourcemac': 'devmac'}, inplace=True)
    # Rename for internal consistancy

    extDataRows = dataDf.loc[:, ['devmac', 'ts_sec', 'lat', 'lon']]
    # Main table for Bluetooth where we find: 
    # What | When | LAT | LON |
    extDataRows['signal'] = -40
    # Kismet does not record signal strenght of bluetooth devices on capture so -40 DBM is the average for a bluetooth connection which would be needed to record a device
    

    # Calculate period of time device was seen
    periodSeen = []
    for row in extDevRows.itertuples():
        result = row[3] - row[2]
        periodSeen.append(result)

    extDevRows['period'] = periodSeen
    extDevRows.drop('first_time', axis=1, inplace=True)
    extDevRows.drop('last_time', axis=1, inplace=True)

    # Combine both dataframes of wifi and bluetooth
    combineData = pd.concat([extPackRows, extDataRows])

    # Attached period seen to both bluetooth and wifi
    combineDataMerge = pd.merge(combineData, extDevRows, on='devmac', how='left')
    
    # Get user input
    userInput = input("Enter MAC address sperated by commas or spaces: ")

    macList = [mac.strip() for mac in re.split(r'[,\s]+', userInput) if mac]

    validMacList = valid_mac_adddress(macList)

    # Add new label row
    combineDataMerge['label'] = np.nan # Fill with black values since we need user input to find the stalking device

    # Find stalker MAC and Label devices
    combineDataMerge['label'] = combineDataMerge['devmac'].apply(lambda x: 1 if x in validMacList else 0)
    combineDataMerge['label'] = combineDataMerge['label'].replace({0: 'benign', 1: 'malicious'})

    # Write and append to a .CSV
    csvDataFile = 'data.csv'


    combineDataMerge.to_csv(csvDataFile, index=False, mode='a', header=not pd.io.common.file_exists(csvDataFile))

if __name__=="__main__":
    main()