from django.urls import include, path
from . import views 
from rest_framework import routers
#from .views import index
from arg.views import RegionViewSet, EnvironmentalActivityViewSet, DatapointViewSet, SubRegionViewSet, UntrackedRegionViewSet

router = routers.DefaultRouter()
router.register(r'region', RegionViewSet)
router.register(r'environmentalactivity', EnvironmentalActivityViewSet)
router.register(r'datapoint', DatapointViewSet)
router.register(r'subregion', SubRegionViewSet)
router.register(r'untrackedregion', UntrackedRegionViewSet)

#URLConf
urlpatterns = [
     path('hello/', views.say_hello),
     path('api/', views.api_home),
     path('models/', include(router.urls)),
     path('geojson/', views.geojson_home),
     path('setcookie/', views.api_home),
     path('getcookie/', views.api_home)
]


# curl -X POST http://127.0.0.1:8000/arg/geojson/ -H "Content-Type: application/json" -d '{"ea": "temperature", "datetime": "2022-11-13T00:00:00"}'