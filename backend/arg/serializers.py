from rest_framework import serializers
from arg.models import Region, Datapoint, EnvironmentalActivity, User, Notification



#class UserSerializer(serializers.ModelSerializer):

 #   class Meta:
 #       model = User
 #       fields = ['id', 'username', 'email', 'is_active', 'created', 'updated']
 #       read_only_field = ['is_active', 'created', 'updated']

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('region_name', 'latitude', 'longitude')

class EnvironmentalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalActivity
        fields = ('ea_name',)

class DatapointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datapoint
        fields = ('dp_id', 'region', 'ea', 'dp_datetime', 'is_future', 'value')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'hashed_password')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('notification_id', 'email', 'ea', 'region', 'threshold', 'mode')
