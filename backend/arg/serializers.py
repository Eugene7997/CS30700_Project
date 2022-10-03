from rest_framework import serializers
from arg.models import Region, Datapoint, EnvironmentalActivity

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('region_id', 'region_name', 'latitude', 'longitude')

class EnvironmentalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalActivity
        fields = ('ea_id', 'ea_name')

class DatapointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datapoint
        fields = ('dp_id', 'region_id', 'ea_id', 'dp_datetime', 'is_future', 'value')