from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import JsonResponse
import reverse_geocode

from arg.serializers import RegionSerializer, DatapointSerializer, EnvironmentalActivitySerializer, SubRegionSerializer, UntrackedRegionSerializer
from arg.models import Region, Datapoint, EnvironmentalActivity, SubRegion, UntrackedRegion
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from geopy.geocoders import Nominatim
from django.forms import Form

# Create your views here.
# request -> response
# request handler 

DEBUG_MODE = 1

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

class SubRegionViewSet(viewsets.ModelViewSet):
    queryset = SubRegion.objects.all()
    serializer_class = SubRegionSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        subregion = request.data['subregion_name']
        UntrackedRegion.objects.filter(untrackedregion_name=subregion).delete()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class UntrackedRegionViewSet(viewsets.ModelViewSet):
    queryset = UntrackedRegion.objects.all()
    serializer_class = UntrackedRegionSerializer

@api_view(["GET", "POST"])

def api_home(request, *args, **kwargs):
    temp = 0
    #humidity = 0
    if request.method == 'GET':
        return JsonResponse({"error": "only send latitude/longitude post requests to this URL"})
    if request.method == 'POST':
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')
        temp = latlon_to_temp(lat, lon)
        #humidity = latlon_to_humidity(lat, lon)
        return JsonResponse({"temperature": temp})
    #return JsonResponse({"region": serializer.data.region_name})

def latlon_to_temp(lat, lon):
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
    coordinates = (lat, lon),
    loc = reverse_geocode.search(coordinates)
    country = loc[0]['country']
    if(DEBUG_MODE):
        print("country:")
        print(country)
    try:
         #see if country is a primary region
        reg = Region.objects.get(region_name=country)
    except:
        try: 
             #see if country is a sub region
            reg = SubRegion.objects.get(subregion_name=country).region
            if(DEBUG_MODE):
                print("region: ")
                print(reg.region_name)
        except:
            if not UntrackedRegion.objects.filter(untrackedregion_name=country).exists():
                untracked = UntrackedRegion()
                untracked.untrackedregion_name = country
                untracked.save()
            return {'error': 'region not tracked in database'}
    try:
        dp = Datapoint.objects.get(region_id = reg)
    except:
        return {'error': 'no data for this region'}
    return {'temperature': dp.value}

def latlon_to_humidity(lat, lon):
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
    coordinates = (lat, lon),
    loc = reverse_geocode.search(coordinates)
    country = loc[0]['country']
    try:
        # see if country is a primary region
        reg = Region.objects.get(region_name=country)
    except:
        try: 
            # see if country is a sub region
            reg = SubRegion.objects.get(subregion_name=country).region
        except:
            if not UntrackedRegion.objects.filter(untrackedregion_name=country).exists():
                untracked = UntrackedRegion()
                untracked.untrackedregion_name = country
                untracked.save()
            return {'error': 'region not tracked in database'}
    try:
        dp = Datapoint.objects.get(region_id = reg)
    except:
        return {'error': 'no data for this region'}
    return {'humidity': dp.value}