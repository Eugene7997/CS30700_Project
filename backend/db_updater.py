from asyncio import DatagramProtocol
import schedule
import time
import random
import json
import mysql.connector
import datetime
import random
from api_calls import *

def update_db():
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
            api_data = call_api(eas, lat, lon)
            data[region] = api_data
        connection.close()
        return data
    return None

        

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


schedule.every(1).hours.do(update_db)

while True:
    schedule.run_pending()
    time.sleep(1)

