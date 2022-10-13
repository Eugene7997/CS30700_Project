from rest_framework import serializers
from arg.models import Region, Datapoint, EnvironmentalActivity, SubRegion, UntrackedRegion

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('region_name', 'latitude', 'longitude')

class EnvironmentalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalActivity
        fields = ('ea_name')

class DatapointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datapoint
        fields = ('dp_id', 'region', 'ea', 'dp_datetime', 'is_future', 'value')

class SubRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubRegion
        fields = ('subregion_name', "region")

class UntrackedRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UntrackedRegion
        fields = ('untrackedregion_name',)