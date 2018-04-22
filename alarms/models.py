from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # The unique ID for each physical clock. One clock per account.
    clock = models.CharField(max_length=32)
    # The User that owns this profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.user.__str__()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
    # Time the alarm should go off
    time = models.TimeField()
    # An optional label
    label = models.CharField(max_length=256)
    # The start and end points for the route, respectively
    origin = models.CharField(max_length=512)
    destination = models.CharField(max_length=512)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # Whether the alarm repeats or not for a given day
    sunRepeat = models.BooleanField(default=False)
    monRepeat = models.BooleanField(default=False)
    tueRepeat = models.BooleanField(default=False)
    wedRepeat = models.BooleanField(default=False)
    thuRepeat = models.BooleanField(default=False)
    friRepeat = models.BooleanField(default=False)
    satRepeat = models.BooleanField(default=False)

    def __str__(self):
        return self.label
