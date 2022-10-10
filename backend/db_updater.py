from asyncio import DatagramProtocol
import schedule
import time
import random
import json
import mysql.connector
import datetime

def update_db():
    data = generate_placeholder_data()
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='12345')
    except Exception as e:
        print("error while connecting to MySQL")
    finally:
        if connection.is_connected():
            cursor = connection.cursor()
            for region in data:
                region_dict = data[region]
                for ea in region_dict:
                    ea_val = region_dict[ea]
                    query = "INSERT INTO datapoint (dp_id, region_id, ea_id, dp_datetime, is_future, value) VALUES (%s, %s, %s, %s, %s, %d)"
                    val = [0, region, ea, time, 0, ea_val]
                    cursor.executemany(connection, val)
            connection.commit()






def generate_placeholder_data():
    regions = ['north america', 'south america', 'europe', 'africa', 'asia', 'oceania']
    eas = ['temperature', 'earthquake frequency', 'rainfall', 'climate']
    data = {region: {} for region in regions}
    for region in regions:
        for ea in eas:
            if random.uniform(0, 1) <= 0.95:
                datapoint = random.uniform(0, 255)
                data[region][ea] = datapoint
            else:
                 data[region][ea] = -1
    return data


'''
SQL connection template:

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='djangodatabase',
                                         user='dbadmin',
                                         password=12345)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Exception as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL Connection closed")
'''

schedule.every(1).minutes.do(update_db)

while True:
    schedule.run_pending()
    time.sleep(1)