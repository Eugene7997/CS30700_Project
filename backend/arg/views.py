from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import JsonResponse
import reverse_geocode
from django.db.models import Min, Max
from django.http import HttpResponse

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
import hashlib
import re

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
# request -> response
# request handler

DEBUG_MODE = 1



def setcookie(request):
    html = HttpResponse("<h1>Dataflair Django Tutorial</h1>")
    if request.COOKIES.get('visits'):
        html.set_cookie('tabstyle', 'Welcome Back')
        value = int(request.COOKIES.get('visits'))
        html.set_cookie('visits', value + 1)
    else:
        value = 1
        text = "Welcome for the first time"
        html.set_cookie('visits', value)
        html.set_cookie('tabstyle', text)
    return html

#def showcookie(request):
#    if request.COOKIES.get('visits') is not None:
#        value = request.COOKIES.get('visits')
#        text = request.COOKIES.get('dataflair')
#        html = HttpResponse("<center><h1>{0}<br>You have requested this page {1} times</h1></center>".format(text, value))
#        html.set_cookie('visits', int(value) + 1)
#        return html
#    else:
#       return redirect('/setcookie')

    



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

def home(request, template):
    response = render(request, template)  # django.http.HttpResponse
    response.set_cookie(key='id', value=1)
    return response

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

def getRoutes(request):
    routes = ['/api/auth',
            '/api/create']
    return JsonResponse(routes, safe=False)

@api_view(["GET", "POST"])
@csrf_exempt
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
@csrf_exempt
def geojson_home(request, *args, **kwargs):
    permission_classes = [permissions.IsAuthenticated]
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
        matching_users = User.objects.filter(email=user_email)
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
        identical_notifications = Notification.objects.filter(user=db_user, ea=db_ea, region=db_region, threshold=threshold, mode=mode)
        if len(identical_notifications) != 0:
            return JsonResponse({"Status": "Failure: A notification with these parameters already exists for this user"})
        Notification.objects.create(user=db_user, ea=db_ea, region=db_region, threshold=threshold, mode=mode)
        return JsonResponse({"Status": "Success"})
    return JsonResponse({"error": request.method + " is not a valid request method for this URL. Use POST or GET."})

# use this command to test /arg/notifications/, will require an entry in the User table with email set to "test@mail.com"
#curl -X POST -H "Content-Type: application/json" -d '{"email": "test@gmail.com", "ea": "temperature", "region": "Africa", "threshold": 100.5, "mode": "less"}' http://127.0.0.1:8000/arg/notifications/

@api_view(["GET", "POST"])
def delete_notification(request, *args, **kwargs):
    if request.method == 'GET':
        return JsonResponse({"error": "only send post requests with json data in format {'email': string, 'region': string, 'ea': string, 'mode': string, 'threshold': float} to this URL"})
    if request.method == 'POST':
        user = request.data.get('email')
        region = request.data.get('region')
        ea = request.data.get('ea')
        mode = request.data.get('mode')
        threshold = request.data.get('threshold')
        matching_notifications = Notification.objects.filter(user=user, region=region, ea=ea, mode=mode, threshold=threshold)
        if len(matching_notifications) == 0:
            return JsonResponse({"Status": "Failure: This notification does not exist."})
        try:
            matching_notifications.delete()
        except:
            return JsonResponse({"Status": "Failure: Encountered an error deleting the value from the database."})
        return JsonResponse({"Status": "Success"})
    return JsonResponse({"error": request.method + " is not a valid request method for this URL. Use POST or GET."})


@api_view(["GET", "POST"])
def list_notifications(request, *args, **kwargs):
    if request.method == 'GET':
        return JsonResponse({"error": "only send post requests with json data in format {'email': string} to this URL"})
    if request.method == 'POST':
        user_email = request.data.get('email')
        user_notifications = Notification.objects.filter(user=user_email)
        response_notifications = []
        for notif_object in user_notifications:
            response_notifications.append({"notification_id": notif_object.notification_id, 
                                           "ea": notif_object.ea,
                                           "region": notif_object.region,
                                           "mode": notif_object.mode,
                                           "threshold": notif_object.threshold})
        return JsonResponse(response_notifications)
    return JsonResponse({"error": request.method + " is not a valid request method for this URL. Use POST or GET."})


@api_view(["GET", "POST"])
def login_home(request, *args, **kwargs):
    if request.method == 'GET':
        return JsonResponse({"error": "only send post requests with json data in format {'email': string, 'password': string}"})
    if request.method == 'POST':
        user_email = request.data.get('email')
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(email_regex, user_email):
            return JsonResponse({"error": "Invalid email address"})
        unhashed_password = request.data.get('password')
        hashed_password = hashlib.sha256(unhashed_password.encode()).hexdigest()
        matching_users = User.objects.filter(email=user_email)
        if len(matching_users) == 0:
            return JsonResponse({"error": "User does not exist"})
        user = matching_users[0]
        if hashed_password != user.hashed_password:
            return JsonResponse({"error": "Password is incorrect"})
        return JsonResponse({"success": "Username and password are valid"})
    return JsonResponse({"error": request.method + " is not a valid request method for this URL. Use POST or GET."})


@api_view(["GET", "POST"])
def register_home(request, *args, **kwargs):
    if request.method == 'GET':
        return JsonResponse({"error": "only send post requests with json data in format {'email': string, 'password': string, 'username': string}"})
    if request.method == 'POST':
        user_email = request.data.get('email')
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(email_regex, user_email):
            return JsonResponse({"error": "Invalid email address"})
        unhashed_password = request.data.get('password')
        hashed_password = hashlib.sha256(unhashed_password.encode()).hexdigest()
        matching_users = User.objects.filter(email=user_email)
        matching_users = User.objects.filter(email=user_email)
        if len(matching_users) != 0:
            return JsonResponse({"error": "That email address is already in use"})
        User.objects.create(email=user_email, hashed_password=hashed_password)
        return JsonResponse({"success": "User has been registered"})
    return JsonResponse({"error": request.method + " is not a valid request method for this URL. Use POST or GET."})
    

#curl -X POST -H "Content-Type: application/json" -d '{"email": "acrutled@purdue.edu", "password": "password1", "mode": "register"}' http://127.0.0.1:8000/arg/login/

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