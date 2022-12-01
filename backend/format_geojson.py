import json
import datetime
import sys
import os
from pycountry_convert import country_alpha2_to_continent_code, country_alpha3_to_country_alpha2, country_name_to_country_alpha2
import mysql.connector



continent_dict = {
    'NA': 'North America',
    'OC': 'Oceania',
    'AF': 'Africa',
    'EU': 'Europe',
    'SA': 'South America',
    'AS': 'Asia',
    'AQ': 'Antarctica'
}


def populate_geojson(data):
    if data is None:
        return {"error": "no values for the date selection"}
    f = open('countries.geojson')
    template = json.load(f)
    for i in range(len(template['features'])):
        country_json = template['features'][i]
        a3_code = str(country_json['properties']['ISO_A3'])
        a2_code = None

        try:
            try:
                a2_code = country_alpha3_to_country_alpha2(a3_code)
            except:
                country_name = country_json['properties']['ADMIN']
                a2_code = country_name_to_country_alpha2(country_name)
        except:
            template['features'][i] = None
            continue
        try:
            continent_code = country_alpha2_to_continent_code(a2_code)
        except:
            if a2_code == 'AQ':
                continent_code = 'AQ'
            else:
                template['features'][i] = None
                continue
        if continent_code == 'AN':
            continent_code = 'AQ'
        val = data[continent_code]
        template['features'][i]['properties']['value'] = val

    template['features'] = [i for i in template['features'] if i is not None]
    return template



def get_world_data(ea, time, end_time=None):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='djangodatabase',
                                             user='dbadmin',
                                             password='password12345')
    except Exception as e:
        print("error while connecting to MySQL: " + str(e))
        return
    
    values = {}
    cursor = connection.cursor()
    if end_time is None:
        for continent_code in continent_dict.keys():
            query = "SELECT * FROM arg_datapoint WHERE is_future = 0 AND region_id = %s AND ea_id = %s AND dp_datetime < %s ORDER BY arg_datapoint.dp_datetime DESC LIMIT 1;"
            vals = [continent_dict[continent_code], ea, time]
            cursor.execute(query, vals)
            responses = cursor.fetchall()
            if len(responses) == 0:
                return None
            row = responses[0]
            value = row[3]
            values[continent_code] = value
    else:
        for continent_code in continent_dict.keys():
            query = "SELECT * FROM arg_datapoint WHERE is_future = 0 AND region_id = %s AND ea_id = %s AND dp_datetime < %s AND dp_datetime > %s;"
            vals = [continent_dict[continent_code], ea, end_time, time]
            cursor.execute(query, vals)
            responses = cursor.fetchall()
            if len(responses) == 0:
                if continent_code == 'AQ':
                    values[continent_code] = 0
                    continue
                else:
                    return None
            avg = sum([response[3] for response in responses]) / len(responses)
            values[continent_code] = avg
    connection.close()
    return values