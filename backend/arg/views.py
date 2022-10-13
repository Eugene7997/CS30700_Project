from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import JsonResponse
from geopy.geocoders import Nominatim

from arg.serializers import RegionSerializer, DatapointSerializer, EnvironmentalActivitySerializer
from arg.models import Region, Datapoint, EnvironmentalActivity

# Create your views here.
# request -> response
# request handler 

def say_hello(request):
    #pull data from db
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

def api_home(request, *args, **kwargs):
    lat = 51.507351
    lon = -0.127758
    # TODO: (Sahiti) setup request to take latitude and longitude as inputs
    

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(lat)+","+str(lon))
    loc_dic = location.raw['address']
    country = loc_dic['country']
    reg = Region.objects.get(region_name=country)

    temp = 0
    #TODO: (Adam) given latitude and longitude, find temperature of corresponding region

    return JsonResponse({"temp": temp})