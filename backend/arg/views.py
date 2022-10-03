from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

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