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

LOCAL_UTC_OFFSET = -4 # change this to -5 when edt turns to est

def update_db(backfill = True):
    print("updating at: " + str(datetime.datetime.now(datetime.timezone.utc)) + " UTC")
    data = fetch_data()
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL: " + str(e))
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
    if backfill and datetime.datetime.now(datetime.timezone.utc).hour == 0:
        fill_gaps()


def fetch_data():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL: " + str(e))
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
            parser = api_parser() #make sure you only define one of these per region, otherwise time saving features will break
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
                if ea in lat_lon_overrides[region].keys():
                    ovr_lat = lat_lon_overrides[region][ea][0]
                    ovr_lon = lat_lon_overrides[region][ea][1]
                    data[region][ea] = ea_map[ea](ovr_lat, ovr_lon)
                else:
                    data[region][ea] = ea_map[ea](lat, lon)
        connection.close()
        return data
    return None


def fill_gaps():
    try: 
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL: " + str(e))
    missing_points = get_missing_datapoints()
    if missing_points is None:
        return
    for region in missing_points.keys():
        default_lat = 0
        default_lon = 0
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM arg_region WHERE region_name = %s;", [region])
            region_tuple = cursor.fetchall()[0]
            default_lat = region_tuple[1]
            default_lon = region_tuple[2]
        else:
            print("failed: MySQL disconnected")
            return
        backfiller = api_backfill()
        ea_map = {
            'temperature': backfiller.temperature,
            'humidity': backfiller.humidity,
        }
        for ea in missing_points[region].keys():
            if not ea in ea_map.keys():
                continue
            if ea in lat_lon_overrides[region].keys():
                lat = lat_lon_overrides[region][ea][0]
                lon = lat_lon_overrides[region][ea][1]
            else:
                lat = default_lat
                lon = default_lon
            end_time = datetime.datetime.now(datetime.timezone.utc)
            start_time = end_time - datetime.timedelta(days=1)
            hourly_data = ea_map[ea](lat, lon, start_time, end_time)
            fill_in(hourly_data, missing_points[region][ea], region, ea)


def fill_in(hourly_data, missing_datapoints, region, ea):
    now = datetime.datetime.now(datetime.timezone.utc)
    target_date_utc = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=1)
    target_date_local = target_date_utc + datetime.timedelta(hours=LOCAL_UTC_OFFSET)
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL: " + str(e))
    if connection.is_connected():
        cursor = connection.cursor()
        for hour in missing_datapoints:
            value = hourly_data[hour]
            date_hour = target_date_local + datetime.timedelta(hours=hour)
            vals = [date_hour, 0, value, ea, region]
            cursor.execute("INSERT INTO arg_datapoint (dp_datetime, is_future, value, ea_id, region_id) VALUES (%s, %s, %s, %s, %s);", vals)
        cursor.execute("DELETE FROM arg_datapoint WHERE dp_datetime >= %s and dp_datetime < %s and value is NULL;", [target_date_local, target_date_local + datetime.timedelta(days=1)])
        connection.commit()


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
        now = datetime.datetime.now(datetime.timezone.utc)
        # need to account for local UTC offset since we're using this to query our local database
        time_max = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=LOCAL_UTC_OFFSET)
        time_min = time_max - datetime.timedelta(days=1)
        cursor.execute("SELECT * FROM arg_datapoint WHERE dp_datetime >= %s and dp_datetime < %s and is_future = 0 and value is not NULL;", [time_min, time_max])
        datapoints_past_day = cursor.fetchall()
        missing_points = {}
        for region_tuple in supported_regions:
            region = region_tuple[0]
            missing_points[region] = {}
            for ea_tuple in supported_eas:
                ea = ea_tuple[0]
                # get all of the times for the region/ea pair in the database
                # Also need to convert times to UTC to correspond with fetched data, so we do the subtraction and get remainder
                existing_hours = [(point_tuple[1].hour - LOCAL_UTC_OFFSET) % 24 for point_tuple in datapoints_past_day if (point_tuple[4] == ea and point_tuple[5] == region)]
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
    print("Running in hourly mode. First database update will be in 1 hour.")
    schedule.every(1).hours.do(update_db)
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    print("mode \"" + mode + "\" is not recognized.")
    print("Run \"db_updater.py help\" for a list of modes")
