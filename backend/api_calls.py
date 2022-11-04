import requests
import datetime
import mysql.connector
import reverse_geocode
from geopy.geocoders import Nominatim

lat_lon_overrides = {
    'North America': {},
    'South America': {
        'sea level': [-1.167, -48.467],
        'ozone': [-15.833, -47.9],
        'no2': [-15.833, -47.9],
        'co2': [-12.046374, -77.042793],
    },
    'Europe': {
        'ozone': [52.5213, 13.4096],
        'no2': [52.5213, 13.4096],
    },
    'Africa': {
        'sea level': [3.467, 8.55],
        'co2': [-28.4792625, 24.6727135],
        'ozone': [30.0443992615, 31.2357196808],
        'no2': [30.0443992615, 31.2357196808],
    },
    'Asia': {
        'sea level': [33.533, 126.55],
        'co2': [33.533, 126.55],
        'ozone': [39.928353, 116.416357],
        'no2': [39.928353, 116.416357],
    },
    'Oceania': {
        'sea level': [-14.1, 126.7],
        'ozone': [-35.2788, 149.1417],
        'no2': [-35.2788, 149.1417],
    },
    'Antarctica': {
        'sea level': [-64.333, -62.983],
        'co2': [-34.603722, -58.381592],
        'ozone': [-22.2139, -65.2528],
        'no2': [-22.2139, -65.2528],
    },
    
}

class api_parser:
    def __init__(self):
        self.temp_humid_response = None
        self.ozone_no2_response = None

    def temperature(self, lat, lon):
        temp_URL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid=37cde85ed34605798aa360d4c26dc586&units=metric".format(lat, lon)
        if self.temp_humid_response is None:
            r = requests.get(url=temp_URL)
            self.temp_humid_response = r.json()
        if not 'main' in self.temp_humid_response.keys():
            return None
        return self.temp_humid_response['main']['temp']
    
    def humidity(self, lat, lon):
        humid_URL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid=37cde85ed34605798aa360d4c26dc586&units=metric".format(lat, lon)
        if self.temp_humid_response is None:
            r = requests.get(url=humid_URL)
            self.temp_humid_response = r.json()
        if not 'main' in self.temp_humid_response.keys():
            return None
        return self.temp_humid_response['main']['humidity']

    def co2(self, lat, lon):
        #return None # comment this out when doing important demo tests
        co2_URL = "https://api.co2signal.com/v1/latest?lon={1}&lat={0}".format(lat, lon)
        co2_headers = {'auth-token': 'S3Hlk9xkYNaGmqYn8G1JoIH0QPiJsn55'}
        r = requests.get(url=co2_URL, headers=co2_headers)
        if not 'data' in r.json().keys():
            return None
        return r.json()['data']['fossilFuelPercentage']

    def sea_level(self, lat, lon):
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
            coordinates = (lat, lon),
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
        sea_level_URL = "https://www.worldtides.info/api/v3?heights&date={0}&lat={1}&lon={2}&key=2ff4df9a-2263-4c2c-a8b8-e8c11d46331f".format(datetime.datetime.now().date(), lat, lon)
        r = requests.get(url=sea_level_URL).json()
        if not 'heights' in r.keys():
            return None
        return r['heights'][0]['height']
    
    def ozone(self, lat, lon):
        if self.ozone_no2_response is None:
            ozone_URL = "https://api.ambeedata.com/latest/by-lat-lng?lat={0}&lng={1}".format(lat, lon)
            ozone_headers = {"x-api-key": "b1637cd664e7dce01cbd651b44e311e27b269c4717eb903fe290388116354b69"}
            r = requests.get(url=ozone_URL, headers=ozone_headers)
            self.ozone_no2_response = r.json()
        if not 'stations' in self.ozone_no2_response.keys():
            return None
        return self.ozone_no2_response['stations'][0]['OZONE']

    def no2(self, lat, lon):
        if self.ozone_no2_response is None:
            no2_URL = "https://api.ambeedata.com/latest/by-lat-lng?lat={0}&lng={1}".format(lat, lon)
            no2_headers = {"x-api-key": "b1637cd664e7dce01cbd651b44e311e27b269c4717eb903fe290388116354b69"}
            r = requests.get(url=no2_URL, headers=no2_headers)
            self.ozone_no2_response = r.json()
        if not 'stations' in self.ozone_no2_response.keys():
            return None
        return self.ozone_no2_response['stations'][0]['NO2']
        
class api_backfill:
    def __init__(self):
        self.temp_humid_response = None
    
    def temperature(self, lat, lon, start, end):
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{0}%2C{1}/{2}/{3}?unitGroup=us&key=CMQ8N7SN9FBHRMXSDKK86GYYN&include=hours".format(lat, lon, start.date(), end.date())
        if self.temp_humid_response is None:
            r = requests.get(url=url)
            self.temp_humid_response = r.json()
        hourly = self.temp_humid_response['days'][0]['hours']
        temps = {int(hour['datetime'][0:2]): hour['temp'] for hour in hourly}
        return temps
    
    def humidity(self, lat, lon, start, end):
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{0}%2C{1}/{2}/{3}?unitGroup=us&key=CMQ8N7SN9FBHRMXSDKK86GYYN&include=hours".format(lat, lon, start.date(), end.date())
        if self.temp_humid_response is None:
            r = requests.get(url=url)
            self.temp_humid_response = r.json()
        hourly = self.temp_humid_response['days'][0]['hours']
        # formatted like {0:10, 1:15, 2:27.3, 3:0.4} where each key is an hour and each value is a humidity
        humids = {int(hour['datetime'][0:2]) : hour['humidity'] for hour in hourly}
        return humids
