import requests
import datetime
import mysql.connector
import reverse_geocode

class api_parser:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.temp_humid_URL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid=37cde85ed34605798aa360d4c26dc586&units=metric".format(lat, lon)
        self.co2_URL = "https://api.co2signal.com/v1/latest?lon={1}&lat={0}".format(lat, lon)
        self.co2_headers = {'auth-token': 'S3Hlk9xkYNaGmqYn8G1JoIH0QPiJsn55'}
        self.ozone_no2_URL = "https://api.ambeedata.com/latest/by-lat-lng?lat={0}&lng={1}".format(lat, lon)
        self.sea_level_URL = "https://www.worldtides.info/api/v3?heights&date={0}&lat={1}&lon={2}&key=2ff4df9a-2263-4c2c-a8b8-e8c11d46331f".format(datetime.datetime.now().date(), lat, lon)
        self.temp_humid_response = None
        

    def temperature(self):
        if self.temp_humid_response is None:
            r = requests.get(url=self.temp_humid_URL)
            self.temp_humid_response = r.json()
        return self.temp_humid_response['main']['temp']
    
    def humidity(self):
        if self.temp_humid_response is None:
            r = requests.get(url=self.temp_humid_URL)
            self.temp_humid_response = r.json()
        return self.temp_humid_response['main']['humidity']

    def co2(self):
        r = requests.get(url=self.co2_URL, headers=self.co2_headers)
        if not 'data' in r.json().keys():
            return None
        return r.json()['data']['fossilFuelPercentage']

    def sea_level(self):
        existing_sea_level_data = None
        try: 
            connection = mysql.connector.connect(host='localhost',
                                                 database='djangodatabase',
                                                 user='dbadmin',
                                                 password='password12345')
        except Exception as e:
            print("failed to connect to database to look for existing sea level data")
        
        if connection.is_connected():
            # find existing sea level data and return it if exists
            cursor = connection.cursor()
            today = datetime.datetime.now()
            start_of_day = datetime.datetime(today.year, today.month, today.day)
            coordinates = (self.lat, self.lon),
            country = reverse_geocode.search(coordinates)[0]['country']
            cursor.execute("select * FROM arg_subregion WHERE subregion_name = %s;", [country])
            region = cursor.fetchone()
            cursor.execute("select * FROM arg_datapoint WHERE ea_id = 'sea level' and dp_datetime > %s;", [start_of_day])
            sea_level_vals = cursor.fetchall()
            for val_tuple in sea_level_vals:
                val = val_tuple[3]
                if val is not None:
                    return val
            connection.close()
        
        # if we get here, it means that the database did not contain any non-zero value to copy
        r = requests.get(url=self.sea_level_URL).json()
        if not 'heights' in r.keys():
            return None
        return r['heights'][0]['height']
        


def call_api(eas, lat, lon):
    parser = api_parser(lat, lon)
    ea_map = {
        'temperature': parser.temperature,
        'humidity': parser.humidity,
        'co2': parser.co2,
        'sea level': parser.sea_level,
    }
    responses = {}
    for ea in eas:
        if ea not in ea_map.keys(): # skip any eas that aren't accounted for in the function map
            print("Skipping update for unsupported EA: " + ea)
            continue
        responses[ea] = ea_map[ea]()
    return responses