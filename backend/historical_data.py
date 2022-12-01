import pandas as pd
import os
import datetime
import reverse_geocode
import mysql.connector
import json
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2


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
        temperature = df['TAVG'][ind]
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