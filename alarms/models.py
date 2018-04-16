from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # The unique ID for each physical clock. One clock per account.
    clock = models.CharField(max_length=32)

    def __str__(self):
        return self.user


# A Vector is simply a datapoint tracking user experiences
class Vector(models.Model):
    # The data and time of the vector
    time = models.DateTimeField()
    # Number of snoozes it took to wake up
    snoozes = models.IntegerField()
    # Data is decoupled from alarm tables
    alarmtime = models.DateTimeField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.time


class Alarm(models.Model):
    # Date and time the alarm should go off
    date = models.DateTimeField()
    # An optional label
    label = models.CharField(max_length=256)
    # The start and end points for the route, respectively
    origin = models.CharField(max_length=512)
    destination = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Whether the alarm repeats or not
    repeat = models.BooleanField()

    def __str__(self):
        return self.label
