from django.urls import include, path
from . import views 
from rest_framework import routers
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
     path('', include(router.urls)),
     path('api/', views.api_home)
]
