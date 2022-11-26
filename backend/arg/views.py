from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import JsonResponse
import reverse_geocode
from django.db.models import Min, Max

from arg.serializers import RegionSerializer, DatapointSerializer, EnvironmentalActivitySerializer, UserSerializer, NotificationSerializer
from arg.models import Region, Datapoint, EnvironmentalActivity, User, Notification
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from geopy.geocoders import Nominatim
from django.forms import Form

from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import requests
import datetime
import json
import format_geojson
import time
import datetime

# Create your views here.
# request -> response
# request handler

DEBUG_MODE = 1


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


def say_hello(request):
    # pull data from db
    #x = 1
    #y = 2
    return render(request, 'hello.html', {'name': 'Mosh'})


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DatapointViewSet(viewsets.ModelViewSet):
    queryset = Datapoint.objects.all()
    serializer_class = DatapointSerializer


class EnvironmentalActivityViewSet(viewsets.ModelViewSet):
    queryset = EnvironmentalActivity.objects.all()
    serializer_class = EnvironmentalActivitySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    

@api_view(["GET", "POST"])
def api_home(request, *args, **kwargs):
    temp = 0
    humidity = 0
    GHG = 0
    sea = 0
    if request.method == 'GET':
        return JsonResponse({"error": "only send latitude/longitude, EA, and date post requests to this URL"})
    if request.method == 'POST':
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')
        date = request.data.get('date')
        EA = request.data.get('EA')
        valid_eas = ['temperature', 'humidity', 'sea level', 'co2', 'no2', 'ozone']
        if EA not in valid_eas:
            return JsonResponse({"error": EA + " is not a valid environmental activity, must be one of: " + str(valid_eas)})
        value = latlon_to_value(lat, lon, date, EA)
        print("found " + str(value) + " at date: " + str(date))
        return JsonResponse({"Date": date, EA: value})
    return JsonResponse({"error": request.method + " is not a valid request method for this URL. Use POST or GET."})

@api_view(["GET", "POST"])

def geojson_home(request, *args, **kwargs):
    if request.method == 'GET':
        return JsonResponse({"error": "Only send post requests with json data in format {'ea': 'humidity', 'datetime': '2014-09-23T05:46:12'} to this URL"})
    
    if request.method == 'POST':
        ea = request.data.get('ea')
        dt = datetime.datetime.strptime(request.data.get('datetime'), '%Y-%m-%dT%H:%M:%S')
        data = format_geojson.get_world_data(ea, dt)
        geojson = format_geojson.populate_geojson(data)
        return JsonResponse(geojson)
    return JsonResponse({"error": request.method + " is not a valid request method for this URL. Use POST or GET."})


@api_view(["GET", "POST"])

def notifications_home(request, *args, **kwargs):
    if request.method == 'GET':
        return JsonResponse({"error": "only send post requests with json data in format {'email': string, 'ea': string, 'region': string, 'threshold': float, 'mode': string"})
    if request.method == 'POST':
        user_email = request.data.get('email')
        matching_users = User.objects.get(email=user_email)
        if len(matching_users) == 0:
            return JsonResponse({"Status": "Failure: " + user_email + " is not a registered email address."})
        try:
            db_user = matching_users[0]
            ea = request.data.get('ea')
            db_ea = EnvironmentalActivity.objects.get(ea_name=ea)
            region = request.data.get('region')
            db_region = Region.objects.get(region_name=region)
            threshold = request.data.get('threshold')
            mode = request.data.get('mode')
        except:
            return JsonResponse({"Status": "Failure: Failed to fetch specified parameters from the database."})
        Notification.objects.create(user=db_user, ea=db_ea, region=db_region, threshold=threshold, mode=mode)
        return JsonResponse({"Status": "Success"})
    return JsonResponse({"error": request.method + " is not a valid request method for this URL. Use POST or GET."})

def latlon_to_value(lat, lon, date, ea):
    if validate_latlon(lat, lon) is not None: return validate_latlon(lat, lon)
    coordinates = (lat, lon),
    loc = reverse_geocode.search(coordinates)
    country = loc[0]['country']
    try:
        country = country_name_to_country_alpha2(country)
        country = country_alpha2_to_continent_code(country)
        country = cont_alpha2_to_name(country)
    except:
        country = "Antarctica"
    try:
        # see if country is a primary region
        reg = Region.objects.get(region_name=country)
    except:
        return {'error': 'region not tracked in database'}
    try:
        datetime_str = date + " 23:59:59"
        reference_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        db_ea = EnvironmentalActivity.objects.get(ea_name=ea)
        filtered = Datapoint.objects.filter(region=reg, ea=db_ea, is_future=0, dp_datetime__lte=reference_datetime)
        date_of_most_recent = filtered.aggregate(Max('dp_datetime'))['dp_datetime__max']
        datapoint = Datapoint.objects.get(region=reg, ea=db_ea, is_future=0, dp_datetime=date_of_most_recent).value
    except:
        return {'error': 'no ' + ea + ' data for the given region at this date'}
    return {country: datapoint}  # temperature:value


def validate_latlon(lat, lon):
    if lat is None:
        return {'error': 'latitude field required'}
    if lon is None:
        return {'error': 'longitude field required'}
    if type(lat) != type(1) and type(lat) != type(1.):
        return {'error': 'latitude must be a number datatype'}
    if type(lon) != type(1) and type(lon) != type(1.):
        return {'error': 'longitude must be a number datatype'}
    if lat > 90 or lat < -90:
        return {'error': 'latitude range is -90 to 90'}
    if lon > 180 or lon < -180:
        return {'error': 'longitude range is -180 to 180'}
    return None