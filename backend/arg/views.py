from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from django.http import JsonResponse

from arg.serializers import RegionSerializer, DatapointSerializer, EnvironmentalActivitySerializer
from arg.models import Region, Datapoint, EnvironmentalActivity
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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



@api_view(["GET", "POST"])
def api_home(request, *args, **kwargs):
    #request -> HttpRequest -> Django

    if request.method == 'GET':
        reg = Region.objects.all()
        serializer = RegionSerializer(reg, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            lat = serializer.data.region_name
            return Response(lat, status=status.HTTP_201_CREATED)
    #return JsonResponse({"region": serializer.data.region_name})
        
    #reg = Region.objects.get(latitude=8)
    #serializer = RegionSerializer(data=request)
    
    

    