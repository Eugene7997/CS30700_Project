import datetime
import mysql.connector
import json
import time

regions = [('North America', 42, -71), ('South America', -9, -55), ('Europe', 55, 15), ('Africa', -9, 35), ('Asia', 34, 100), ('Oceania', -23, 140), ('Antarctica', -83, 135)]
eas = ['temperature', 'humidity', 'co2', 'sea level', 'ozone', 'no2']
subregions = [('Canada', 'North America'), ('Tanzania, United Republic of', 'Africa'), ('Antarctica', 'Antarctica'),
              ('China', 'Asia'), ('Denmark', 'Europe'), ('United States', 'North America'), ('Australia', 'Oceania'), ('Brazil', 'South America')]


answer = input("WARNING: Running this script will remove ALL data from the database. Do you wish to continue? (y/n)")
if not (answer == 'y' or answer == 'Y'):
    print("aborted")
    exit(1)

print("connecting to db...")
try:
    connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
except Exception as e:
    print("error while connecting to MySQL")
    exit(1)


if connection.is_connected():
    cursor = connection.cursor()
    print("removing existing data...")
    cursor.execute("DELETE FROM arg_datapoint;")
    cursor.execute("DELETE FROM arg_subregion;")
    cursor.execute("DELETE FROM arg_environmentalactivity;")
    cursor.execute("DELETE FROM arg_untrackedregion;")
    cursor.execute("DELETE FROM arg_region;")

    for region in regions:
        query = "INSERT INTO arg_region (region_name, latitude, longitude) VALUES (%s, %s, %s);"
        cursor.execute(query, list(region))
    
    for ea in eas:
        query = "INSERT INTO arg_environmentalactivity (ea_name) VALUES (%s);"
        cursor.execute(query, [ea])
    
    for subregion in subregions:
        query = "INSERT INTO arg_subregion (subregion_name, region_id) VALUES (%s, %s);"
        cursor.execute(query, list(subregion))

    connection.commit()
    print("successfully added starting data to database")