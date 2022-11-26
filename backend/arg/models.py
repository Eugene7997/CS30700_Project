
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
    region_name = models.CharField(max_length=30, primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)


class EnvironmentalActivity(models.Model):
    ea_name = models.CharField(max_length=50, primary_key=True)


class Datapoint(models.Model):
    dp_id = models.AutoField(primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    ea = models.ForeignKey(EnvironmentalActivity, on_delete=models.CASCADE)
    dp_datetime = models.DateTimeField()
    is_future = models.BooleanField()
    value = models.FloatField(null = True)


class User(models.Model):
    email = models.CharField(max_length=320, primary_key=True)
    hashed_password = models.CharField(max_length=64)


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ea = models.ForeignKey(EnvironmentalActivity, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    threshold = models.FloatField()
    mode = models.CharField(max_length=20)
