
from django.db import models
from django.forms import ModelForm

# MySQL password: 307team19argus
# Create your models here.


# Import your UserLocation model


# Create your forms here
class UserLocation(ModelForm):
    class Meta:
        #model = UserLocation
        fields = ('latitude', 'longitude')

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=30)
    latitude = models.IntegerField()
    longitude = models.IntegerField()

class SubRegion(models.Model):
    subregion_id = models.AutoField(primary_key=True)
    subregion_name = models.CharField(max_length=50)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)

class EnvironmentalActivity(models.Model):
    ea_id = models.AutoField(primary_key=True)
    ea_name = models.CharField(max_length=50)

class Datapoint(models.Model):
    dp_id = models.AutoField(primary_key=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    ea_id = models.ForeignKey(EnvironmentalActivity, on_delete=models.CASCADE)
    dp_datetime = models.DateTimeField()
    is_future = models.BooleanField()
    value = models.FloatField()

class UntrackedRegion(models.Model):
    untrackedregion_id = models.AutoField(primary_key=True)
    untrackedregion_name = models.CharField(max_length=50)