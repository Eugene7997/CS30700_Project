from django.db import models

# MySQL password: 307team19argus
# Create your models here.


class Region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    region_name = models.CharField(max_length=30)
    latitude = models.IntegerField()
    longitude = models.IntegerField()

class EnvironmentalActivity(models.Model):
    ea_id = models.IntegerField(primary_key=True)
    ea_name = models.CharField(max_length=50)

class Datapoint(models.Model):
    dp_id = models.IntegerField(primary_key=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    ea_id = models.ForeignKey(EnvironmentalActivity, on_delete=models.CASCADE)
    dp_datetime = models.DateTimeField()
    is_future = models.BooleanField()
    value = models.FloatField()
