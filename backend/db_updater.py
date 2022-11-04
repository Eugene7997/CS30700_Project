from asyncio import DatagramProtocol
import schedule
import time
import random
import json
import mysql.connector
import datetime
import random
from api_calls import *
import sys


def update_db(backfill = True):
    print("updating...")
    data = fetch_data()
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL")
        return
    if connection.is_connected() and data is not None:
        cursor = connection.cursor()
        for region in data:
            region_dict = data[region]
            for ea in region_dict:
                ea_val = region_dict[ea]
                query = "INSERT INTO arg_datapoint (region_id, ea_id, dp_datetime, is_future, value) VALUES (%s, %s, %s, %s, %s);"
                now = datetime.datetime.now()
                val = [region, ea, now, 0, ea_val]
                cursor.execute(query, val)
        connection.commit()
    if backfill:
        fill_gaps()


def fetch_data():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL")
        return None
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM arg_region;")
        db_regions = cursor.fetchall() # the database response from querying every region in the database, not in clean format
        cursor.execute("SELECT * FROM arg_environmentalactivity")
        db_eas = cursor.fetchall() # the database response from querying every EA in the database, not in clean format
        data = {} # dictionary that will hold all of the current data for every EA and region to later be added to the database
        for region_tuple in db_regions:
            region = region_tuple[0]
            lat = region_tuple[1]
            lon = region_tuple[2]
            eas = [ea_tuple[0] for ea_tuple in db_eas]
            print("getting data for region: " + region)
            parser = api_parser()
            ea_map = {
                'temperature': parser.temperature,
                'humidity': parser.humidity,
                'co2': parser.co2,
                'sea level': parser.sea_level,
                'ozone': parser.ozone,
                'no2': parser.no2
            }
            data[region] = {}
            for ea in eas: 
                print("fetching data for " + ea)
                if ea in lat_lon_overrides[region].keys():
                    ovr_lat = lat_lon_overrides[region][ea][0]
                    ovr_lon = lat_lon_overrides[region][ea][1]
                    data[region][ea] = ea_map[ea](ovr_lat, ovr_lon)
                else:
                    data[region][ea] = ea_map[ea](lat, lon)
                print(data[region][ea])
        connection.close()
        return data
    return None


def fill_gaps():
    missing_points = get_missing_datapoints()
    if missing_points is None:
        return
    for region in missing_points.keys():
        for ea in missing_points[region].keys():
            print("missing " + ea + " in " + region + ": " + str(missing_points[region][ea]))


def get_missing_datapoints():
    has_missing_points = False
    try: 
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL")
        return None
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM arg_region;")
        supported_regions = cursor.fetchall()
        cursor.execute("SELECT * FROM arg_environmentalactivity;")
        supported_eas = cursor.fetchall()
        now = datetime.datetime.now()
        time_cutoff = now - datetime.timedelta(days=1)
        cursor.execute("SELECT * FROM arg_datapoint WHERE dp_datetime > %s and is_future = 0;", [time_cutoff])
        datapoints_past_day = cursor.fetchall()
        missing_points = {}
        for region_tuple in supported_regions:
            region = region_tuple[0]
            missing_points[region] = {}
            for ea_tuple in supported_eas:
                ea = ea_tuple[0]
                # get all of the times for the region/ea pair in the database
                existing_hours = [point_tuple[1].hour for point_tuple in datapoints_past_day if (point_tuple[4] == ea and point_tuple[5] == region)]
                #get every hour from the past day that needs to be filled
                non_existing_hours = [a for a in range(24) if a not in existing_hours]
                if not has_missing_points and len(non_existing_hours) > 0:
                    has_missing_points = True
                missing_points[region][ea] = non_existing_hours
        if not has_missing_points:
            return None
        return missing_points


def generate_placeholder_data():
    regions = ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Oceania', 'Antarctica']
    eas = ['temperature',]
    data = {region: {} for region in regions}
    for region in regions:
        for ea in eas:
            if random.uniform(0, 1) <= 0.95:
                datapoint = random.uniform(0, 255)
                data[region][ea] = datapoint
            else:
                 data[region][ea] = -1
    return data

args = sys.argv

if len(args) < 2:
    print("Not enough arguments. Format: db_updater.py [mode]")
    print("Run \"db_updater.py help\" for a list of modes")
    exit(0)

mode = args[1].lower()

if mode == 'help':
    print("\n\n     -------------------------  Modes  --------------------------\n")
    print("     help  -  lists the possible modes")
    print("     once  -  updates the database once, including back-filling")
    print(" oncenobf  -  updates the database once with no back-filling")
    print(" backfill  -  just runs the back-filling feature of the python script")
    print("   hourly  -  intended production mode, updates the database hourly with back-filling\n\n")
elif mode == 'once':
    update_db()
elif mode == 'oncenobf':
    update_db(backfill = False)
elif mode == 'backfill':
    fill_gaps()
elif mode == 'hourly':
    schedule.every(1).hours.do(update_db)
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    print("mode \"" + mode + "\" is not recognized.")
    print("Run \"db_updater.py help\" for a list of modes")