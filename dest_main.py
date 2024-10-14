#
# main.py - Render UI and hook to commands/functions
#

# Import packages
import os # Execute Shell Commands
import sqlite3
import time
from datetime import datetime
import glob
import json
import pathlib
# from gpsHandler import getdata

# ==================== SETTINGS ====================
POLL_MINUTES = 2
LOG_LINES_TO_SHOW = 20
DEV_TIMES_TO_TRIGGER = 3
SSID_TIMES_TO_TRIGGER = 5
DEVICES_PER_PAGE = 10
ALERTS_PER_PAGE = 10

# =============== CALCULATED VALUES ================
VERSION = "1.0.4"

# get logged in user
user = os.getlogin()
print(user)
# create directories if needed
dest_sub = pathlib.Path('/home/' + user + '/dest_log')
dest_sub.mkdir(parents=True, exist_ok=True)

db_path = '/home/' + user + '/*.kismet' # changed from checking kismet_logs so the specific kismet file can be chosen
# Find Newest DB file
list_of_files = glob.glob(db_path)
latest_file = max(list_of_files, key=os.path.getctime)
print ("Pulling data from: {}".format(latest_file))
con = sqlite3.connect(latest_file) ## kismet DB to point at
if os.path.isfile(latest_file):
    print("File exists")# check that it exists

# Create DB file for storing lists and basic device info
# make db folder if it doesn't exist
dest_db_path = '/home/' + user + '/dest_db'
dest_db_sub = pathlib.Path(dest_db_path)
dest_db_sub.mkdir(parents=True, exist_ok=True)
# create db file
dest_db_fname = '/home/' + user + '/dest_db/dest_db_{}.db'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
# create file
dest_db = sqlite3.connect(dest_db_fname)
dest_db_cursor = dest_db.cursor()
# create devices table
dest_db_cursor.execute('''CREATE TABLE devices (mac text, name text, first_seen int, last_seen int, times_seen int)''')
# create ssids
dest_db_cursor.execute('''CREATE TABLE ssids (ssid text, name text, first_seen int, last_seen int, times_seen int)''')
# create locations
dest_db_cursor.execute('''CREATE TABLE locations (mac text, lat real, lon real, alt real, heading real, timestamp int)''')


# log file as program runs
dest_log_fname = '/home/' + user + '/dest_log/dest_log_{}.txt'.format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
dest_log = open(dest_log_fname, 'w', buffering=1)

dest_log.write("=====[ Destiny v" + VERSION + " ]=====\n")
dest_log.write("Starting at: " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "\n")

def insert_or_update_device(mac, name, first_seen, last_seen):
    global dest_log
    print("Inserting or updating device: " + mac)
    dest_log.write("Inserting or updating device: " + mac + "\n")
    global dest_db_cursor
    # check if device exists
    print("SELECT * FROM devices WHERE mac = '{}'".format(mac))
    dest_db_cursor.execute("SELECT * FROM devices WHERE mac = '{}'".format(mac))
    rows = dest_db_cursor.fetchall()
    if len(rows) > 0:
        # update
        times_seen = rows[0][4] + 1
        print("UPDATE devices SET name = '{}', last_seen = '{}', times_seen = '{}' WHERE mac = '{}'".format(name, last_seen, times_seen, mac))
        dest_db_cursor.execute("UPDATE devices SET name = '{}', last_seen = '{}', times_seen = '{}' WHERE mac = '{}'".format(name, last_seen, times_seen, mac))
    else:
        # insert
        times_seen = 1
        print("INSERT INTO devices VALUES ('{}', '{}', '{}', '{}', '{}')".format(mac, name, first_seen, last_seen, times_seen))
        dest_db_cursor.execute("INSERT INTO devices VALUES ('{}', '{}', '{}', '{}', '{}')".format(mac, name, first_seen, last_seen, times_seen))
    print()


def insert_or_update_ssid(ssid, name, first_seen, last_seen):
    global dest_log
    print("Inserting or updating SSID: " + ssid)
    dest_log.write("Inserting or updating SSID: " + ssid + "\n")
    global dest_db_cursor
    # check if device exists
    print("SELECT * FROM ssids WHERE ssid = '{}'".format(ssid))
    dest_db_cursor.execute("SELECT * FROM ssids WHERE ssid = '{}'".format(ssid))
    rows = dest_db_cursor.fetchall()
    if len(rows) > 0:
        # update
        times_seen = rows[0][4] + 1
        print("UPDATE ssids SET name = '{}', last_seen = '{}', times_seen = '{}' WHERE ssid = '{}'".format(name, last_seen, times_seen, ssid))
        dest_db_cursor.execute("UPDATE ssids SET name = '{}', last_seen = '{}', times_seen = '{}' WHERE ssid = '{}'".format(name, last_seen, times_seen, ssid))
    else:
        # insert
        times_seen = 1
        print("INSERT INTO ssids VALUES ('{}', '{}', '{}', '{}', '{}')".format(ssid, name, first_seen, last_seen, times_seen))
        dest_db_cursor.execute("INSERT INTO ssids VALUES ('{}', '{}', '{}', '{}', '{}')".format(ssid, name, first_seen, last_seen, times_seen))
    print()

def insert_location(mac, lat, lon, alt, heading):
    global dest_log
    print("Inserting location for: " + mac)
    dest_log.write("Inserting location for: " + mac + "\n")
    global dest_db_cursor
    print("INSERT INTO locations VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(mac, lat, lon, alt, heading, int(time.time())))
    dest_db_cursor.execute("INSERT INTO locations VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(mac, lat, lon, alt, heading, int(time.time())))
    print()

def get_device(mac):
    global dest_db_cursor
    dest_db_cursor.execute("SELECT * FROM devices WHERE mac = '{}'".format(mac))
    rows = dest_db_cursor.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return None
    
def get_ssid(ssid):
    global dest_db_cursor
    dest_db_cursor.execute("SELECT * FROM ssids WHERE ssid = '{}'".format(ssid))
    rows = dest_db_cursor.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return None

def get_locations(mac):
    global dest_db_cursor
    dest_db_cursor.execute("SELECT * FROM locations WHERE mac = '{}'".format(mac))
    rows = dest_db_cursor.fetchall()
    if len(rows) > 0:
        return rows[0]
    else:
        return None    

def get_devices(con):
    """
    Get devices from Kismet
    
    Parameters
    ----------
    
    con : sqlite3.Connection
        The connection to the Kismet database
    """
    print("Getting devices...")
    dest_log.write("Getting devices..." + "\n")
    cursorObj = con.cursor()
    # from last X minutes
    cursorObj.execute("SELECT devmac, type, device, last_time FROM devices WHERE last_time > {}".format(time.time() - (POLL_MINUTES * 60)))
    rows = cursorObj.fetchall()
    dest_log.write("Got " + str(len(rows)) + " records from Kismet" + "\n")
    for row in rows:
        
        ssidAdded = False

        raw_device_json = json.loads(str(row[2], errors='ignore'))
        
        # see if there is location data
        if 'kismet.device.base.location' in str(row):
            lat = raw_device_json["kismet.device.base.location"]["kismet.common.location.last"]["kismet.common.location.geopoint"][0]
            lon = raw_device_json["kismet.device.base.location"]["kismet.common.location.last"]["kismet.common.location.geopoint"][1]
            alt = raw_device_json["kismet.device.base.location"]["kismet.common.location.last"]["kismet.common.location.alt"]
            heading = raw_device_json["kismet.device.base.location"]["kismet.common.location.last"]["kismet.common.location.heading"]
            print("Lat: " + str(lat) + " Lon: " + str(lon) + " Alt: " + str(alt) + " Heading: " + str(heading))
            dest_log.write("Lat: " + str(lat) + " Lon: " + str(lon) + " Alt: " + str(alt) + " Heading: " + str(heading) + "\n")
            insert_location(str(row[0]), str(lat), str(lon), str(alt), str(heading))

        # get the name
        dev_name = ''
        if 'kismet.device.base.name' in str(row):
            dev_name = raw_device_json["kismet.device.base.name"]
        
        # if no name, set to unknown
        if dev_name == '':
            dev_name = 'Unknown'
            
        ssid_probed_for = ''
        # check if the key exists
        if 'dot11.probedssid.ssid' in str(row):
            ssid_probed_for = raw_device_json["dot11.device"]["dot11.device.last_probed_ssid_record"]["dot11.probedssid.ssid"]
        if ssid_probed_for == '':
            pass
        else:
            print("Probed SSID: " + ssid_probed_for)
            dest_log.write("Probed SSID: " + ssid_probed_for + "\n")
            ssidAdded = True
            insert_or_update_ssid(ssid_probed_for, dev_name, str(row[3]), str(row[3]))
     
        # check for beacon
        if 'dot11.device.last_beaconed_ssid_record' in str(row):
            # get the ssid
            ssid = raw_device_json["dot11.device"]["dot11.device.last_bssid"]
            print("Beaconed SSID: " + ssid + " | " + dev_name)
            dest_log.write("Beaconed SSID: " + ssid + " | " + dev_name + "\n")
            ssidAdded = True
            insert_or_update_ssid(ssid, dev_name, str(row[3]), str(row[3]))
            
            
        if ssidAdded == False:
            stripped_val = str(row[0]).replace("(","").replace(")","").replace("'","").replace(",","")
            insert_or_update_device(stripped_val, dev_name, str(row[3]), str(row[3]))

# time_count = -1 # so we have a minute to get initial data
time_count = 2
# add label to menu 

# Main Loop
start_time = time.time() - 61 # test

run = True
while run:
    # check if a minute has passed
    cur_time = time.time()
    if (cur_time - start_time) > 60:
        # run code
        start_time = cur_time
        
        # checking if after initial pass
        if time_count == 0:
            print("2 Minute Pass Complete")
            dest_log.write("2 Minute Pass Complete\n")
        if time_count >= 0:
            dest_log.write("Int Time: " + str(time_count) + "\n")
            if time_count % POLL_MINUTES == 0:
                # load the two lists
                get_devices(con)
                # commit the changes
                dest_db.commit()
                # get number of records
                dest_db_cursor.execute("SELECT COUNT(*) FROM devices")
                rows = dest_db_cursor.fetchall()
                print("Total Devices: " + str(rows[0][0]))
                dest_log.write("Total Devices: " + str(rows[0][0]) + "\n")
                dest_db_cursor.execute("SELECT COUNT(*) FROM ssids")
                rows = dest_db_cursor.fetchall()
                print("Total SSIDs: " + str(rows[0][0]))
                dest_log.write("Total SSIDs: " + str(rows[0][0]) + "\n")
                dest_db_cursor.execute("SELECT COUNT(*) FROM locations")
                rows = dest_db_cursor.fetchall()
                print("Total Locations: " + str(rows[0][0]))
                dest_log.write("Total Locations: " + str(rows[0][0]) + "\n")
                    
        time_count += 1
        testGet = get_ssid('F4:02:28:BB:DD:FB')
        print(testGet)