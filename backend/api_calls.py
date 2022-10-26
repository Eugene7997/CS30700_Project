import requests

class api_parser:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.temp_humid_URL = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid=37cde85ed34605798aa360d4c26dc586&units=metric".format(lat, lon)
        self.co2_URL = "https://api.co2signal.com/v1/latest?lon={1}&lat={0}".format(lat, lon)
        self.co2_headers = {'auth-token': 'S3Hlk9xkYNaGmqYn8G1JoIH0QPiJsn55'}
        self.ozone_no2_URL = "https://api.ambeedata.com/latest/by-lat-lng?lat={0}&lng={1}".format(lat, lon)
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
        return r.json()['data']['fossilFuelPercentage']


def call_api(eas, lat, lon):
    parser = api_parser(lat, lon)
    ea_map = {
        'temperature': parser.temperature,
        'humidity': parser.humidity,
        'co2': parser.co2,
    }
    responses = {}
    for ea in eas:
        if ea not in ea_map.keys(): # skip any eas that aren't accounted for in the function map
            continue
        responses[ea] = ea_map[ea]()
    return responses