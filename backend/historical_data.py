import pandas as pd
import os
import datetime
import reverse_geocode
import mysql.connector
import json
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import sys
import random


def cont_alpha2_to_name(input):
    if 'NA' == input:
        return "North America"
    elif 'OC' == input:
        return 'Oceania'
    elif 'AF' == input:
        return 'Africa'
    elif 'EU' == input:
        return 'Europe'
    elif 'SA' == input:
        return 'South America'
    elif 'AS' == input:
        return 'Asia'
        

def process_noaa_temp(df):
    df.dropna(subset=['LATITUDE', 'LONGITUDE', 'DATE', 'TAVG'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL: " + str(e))
        return
    if not connection.is_connected():
        print("error: MySQL disconnected while processing noaa csv")
        return
    cursor = connection.cursor()
    countries = {"United States": "North America",}
    ind_len_str = str(len(df.index))
    for ind in df.index:
        print("(" + str(ind) + "/" + ind_len_str + ")", end="\r")
        lat = df['LATITUDE'][ind]
        lon = df['LONGITUDE'][ind]
        row_date = datetime.datetime.strptime(df['DATE'][ind], '%Y-%m-%d')
        temperature = round(float(df['TAVG'][ind] - 32.0) * (5.0/9.0), 2)
        coordinates = (lat, lon),
        loc = reverse_geocode.search(coordinates)
        country = loc[0]['country']
        if country in countries.keys():
            region = countries[country]
        else:
            region = country_name_to_country_alpha2(country)
            region = country_alpha2_to_continent_code(region)
            region = cont_alpha2_to_name(region)
            countries[country] = region
        arguments = [row_date, 0, float(temperature), "temperature", region]
        cursor.execute("insert into arg_datapoint (dp_datetime, is_future, value, ea_id, region_id) values (%s, %s, %s, %s, %s);", arguments)
    connection.commit()
    connection.close()
    print("(" + ind_len_str + "/" + ind_len_str + ")")

        
def process_owid_co2(df):
    regions = ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Oceania', 'Antarctica']
    df.dropna(subset=['country', 'year', 'co2'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL: " + str(e))
        return
    if not connection.is_connected():
        print("error: MySQL disconnected while processing owid csv")
        return
    cursor = connection.cursor()
    ind_len_str = str(len(df.index))
    for ind in df.index:
        print("(" + str(ind) + "/" + ind_len_str + ")", end="\r")
        region = df['country'][ind]
        if not region in regions:
            continue
        co2 = df['co2'][ind]
        row_date = datetime.datetime(df['year'][ind], 1, 1)
        arguments = [row_date, 0, float(co2), "co2", region]
        cursor.execute("insert into arg_datapoint (dp_datetime, is_future, value, ea_id, region_id) values (%s, %s, %s, %s, %s);", arguments)
    connection.commit()
    connection.close()
    print("(" + ind_len_str + "/" + ind_len_str + ")")

files = [f for f in os.listdir("historicaldata/") if f[-4:] == ".csv"]

def generate_placeholder_historical_data(year):
    ranges = {
        'North America': {
            'temperature': [-8, 23, None],
            'humidity': [0, 100, None],
            'ozone': [0, 50, None],
            'sea level': [0, 10, None],
            'co2': [0, 100, None],
            'no2': [0, 20, None]
        },
        'South America': {
            'temperature': [-10, 20, None],
            'humidity': [0, 100, None],
            'ozone': [0, 50, None],
            'sea level': [0, 10, None],
            'co2': [0, 100, None],
            'no2': [0, 20, None]
        },
        'Europe': {
            'temperature': [-2, 22, None],
            'humidity': [0, 100, None],
            'ozone': [0, 50, None],
            'sea level': [0, 10, None],
            'co2': [0, 100, None],
            'no2': [0, 20, None]
        },
        'Africa': {
            'temperature': [5, 38, None],
            'humidity': [0, 100, None],
            'ozone': [0, 50, None],
            'sea level': [0, 10, None],
            'co2': [0, 100, None],
            'no2': [0, 20, None]
        }, 
        'Asia': {
            'temperature': [-15, 22, None],
            'humidity': [0, 100, None],
            'ozone': [0, 50, None],
            'sea level': [0, 10, None],
            'co2': [0, 100, None],
            'no2': [0, 20, None]
        }, 
        'Oceania': {
            'temperature': [8, 30, None],
            'humidity': [0, 100, None],
            'ozone': [0, 50, None],
            'sea level': [0, 10, None],
            'co2': [0, 100, None],
            'no2': [0, 20, None]
        },
        'Antarctica': {
            'temperature': [-35, -15, None],
            'humidity': [0, 100, None],
            'ozone': [0, 50, None],
            'sea level': [0, 10, None],
            'co2': [0, 100, None],
            'no2': [0, 20, None]
        }
    }
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL: " + str(e))
        return
    if not connection.is_connected():
        print("error: MySQL disconnected while processing noaa csv")
        return
    cursor = connection.cursor()
    start_date = str(year) + "-01-01 23:59:59"
    current_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    previous_dt = current_dt - datetime.timedelta(days=1)
    end_date = "2022-12-01"
    end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    days_passed = 0
    while current_dt < end_dt:
        for region in ranges.keys():
            eas = ranges[region]
            for ea in eas:
                # query DB for any existing values at this point
                existing_query = "SELECT * FROM arg_datapoint WHERE region_id = %s AND ea_id = %s AND dp_datetime > %s AND dp_datetime <= %s;"
                cursor.execute(existing_query, [region, ea, previous_dt, current_dt])
                existing_data = cursor.fetchone()
                cursor.fetchall()
                if existing_data is not None:
                    # set the existing value as the previous value for next time, then continue
                    ranges[region][ea][2] = existing_data[3]
                    continue
                else:
                    # get variables for this step
                    range = eas[ea]
                    low = range[0]
                    high = range[1]
                    step = round(float(high - low) / 10.0, 2)
                    prev = range[2]
                    # if there's no previous value, default to the middle
                    if prev is None:
                        prev = float(high - low) / 2.0
                    # set next value to a random step
                    next_val = prev + random.uniform(-step, step)
                    # cap off next value with the range
                    next_val = round(min(max(next_val, low), high), 2)
                    # set previous value for next time
                    ranges[region][ea][2] = next_val
                    insert_query = "INSERT INTO arg_datapoint (dp_datetime, is_future, value, ea_id, region_id) VALUES (%s, %s, %s, %s, %s);"
                    cursor.execute(insert_query, [current_dt, 0, next_val, ea, region])
        previous_dt = current_dt
        current_dt = current_dt+datetime.timedelta(days=1)
        days_passed += 1
        connection.commit()
        print("days: {0}".format(days_passed), end='\r')
    print("days: {0}".format(days_passed))

'''    data = {region: {} for region in regions}
    for region in regions:
        for ea in eas:
            if random.uniform(0, 1) <= 0.95:
                datapoint = random.uniform(0, 255)
                data[region][ea] = datapoint
            else:
                 data[region][ea] = -1
    return data
    print(year)'''

if len(sys.argv) > 1:
    generate_placeholder_historical_data(sys.argv[1])
else: 
    if len(files) == 0:
        print("No data files in the historical data directory")
        exit(0)

    for file in files:
        filepath = "historicaldata/" + file
        df = pd.read_csv(filepath)
        columns = df.columns.tolist()
        if columns == ['STATION', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'DATE', 'PRCP', 'TAVG', 'TMAX', 'TMIN']:
            # this must be a NOAA temperature CSV
            print("Detected NOAA file: " + file)
            print("Processing valid entries into database...")
            process_noaa_temp(df)
        elif columns[0:8] == ['country', 'year', 'iso_code', 'population', 'gdp', 'cement_co2', 'cement_co2_per_capita', 'co2']:
            # these are columns of an owid co2 data csv
            print("Detected OWID file: " + file)
            print("Processing valid entries into database...")
            process_owid_co2(df)
        print("moving file to used directory")
        os.rename(filepath, "historicaldata/usedhistoricaldata/" + file)