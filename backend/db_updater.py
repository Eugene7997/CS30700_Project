from asyncio import DatagramProtocol
import schedule
import time
import random
import json
import mysql.connector
import datetime
import random

def update_db():
    print("updating...")
    data = generate_placeholder_data()
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL")
    finally:
        if connection.is_connected():
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