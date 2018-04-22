from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from json import loads, JSONDecodeError
from .models import Vector, Alarm, Profile
from .forms import AlarmForm

# TODO (optional): Automatically sync clock set alarms with server


# Allow the user to set new alarms
def setalarms(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = AlarmForm(request.POST)
        if form.is_valid():
            data = request.POST
            print(data)
            # Create the new alarm
            newalarm = Alarm()
            newalarm.label = data["label"]
            newalarm.time = data["time"]
            newalarm.origin = data["origin"]
            newalarm.destination = data["destination"]
            newalarm.sunRepeat = "sunRepeat" in data
            newalarm.monRepeat = "monRepeat" in data
            newalarm.tueRepeat = "tueRepeat" in data
            newalarm.wedRepeat = "wedRepeat" in data
            newalarm.thuRepeat = "thuRepeat" in data
            newalarm.friRepeat = "friRepeat" in data
            newalarm.satRepeat = "satRepeat" in data
            newalarm.user = Profile.objects.get(user=request.user)
            newalarm.save()
            # Redirect to the set alarm page, TODO: Success page
            return HttpResponseRedirect(reverse('setalarm'))
    #TODO: Finish syncing with the pi
    elif request.method == 'PUT':
        print(request.PUT)
        pass
    elif request.method == "GET":
        form = AlarmForm()
    else:
        return HttpResponseRedirect(reverse('home'))
    # TODO: Set up "form" correctly
    return render(request, 'alarms/set.html', {'form': form})


# Show the user his alarms
def viewalarms(request):
    params = {}
    # Check to see if the user is logged in
    if request.user.is_authenticated:
        usr = Profile.objects.get(user=request.user)
        # Get all alarms associated with the user
        alarms = list(Alarm.objects.filter(user=usr))
        # TODO: Make this less hacky
        # Makes a list of tuples of the form:
        #   (label, date, doesrepeat, origin, destination)
        params["alarms"] = []
        print(Alarm.objects.all())
        for a in alarms:
            params["alarms"].append(
                (a.label,
                 a.time,
                 a.sunRepeat,
                 a.monRepeat,
                 a.tueRepeat,
                 a.wedRepeat,
                 a.thuRepeat,
                 a.friRepeat,
                 a.satRepeat,
                 a.origin,
                 a.destination,
                 a.pk,
                 )
            )
        print(params)
        return render(request, 'alarms/list.html', context=params)
    return HttpResponseRedirect(reverse('home'))


# apk is the primary key of the alarm to be deleted
def deletealarms(request, apk):
    alarm = Alarm.objects.get(pk=apk)
    alarm.delete()
    return HttpResponseRedirect(reverse('viewalarms'))


# Get a JSON of all alarms and return it
def getalarms(request, clockid):
    # TODO: Make more meaningful error responses
    if request.method == 'GET':
        # Get all alarms associated with the clockid/user
        try:
            usr = Profile.objects.get(clock=clockid)
        except:
            return HttpResponseBadRequest(request)
        if usr:
            alarms = serializers.serialize("json", Alarm.objects.filter(user=usr))
            # Return all alarms currently set
            return JsonResponse(alarms, safe=False)
        else:
            return HttpResponseBadRequest(request)
    else:
        # An end user will always use a GET, don't need to redirect
        return HttpResponseBadRequest(request)


# receive data from a clock and save it
def recvdata(request):
    if request.method == "POST":
        v = Vector()
        try:
            data = loads(request.body)
            # Populate the Vector fields
            v.time = data["time"]
            v.alarmtime = data["alarmtime"]
            v.snoozes = data["snoozes"]
            usr = Profile.objects.get(clock=data["clockid"])
            # If the clock is unregistered, return a 400 response
            if not usr:
                return HttpResponseBadRequest
            v.user = usr
            # TODO: update this block if/when model changes
        except JSONDecodeError:
            # TODO: Make error reporting better
            return HttpResponseBadRequest
        except KeyError:
            return HttpResponseBadRequest
        except TypeError:
            return HttpResponseBadRequest
        # If the JSON parses fine, then save it and return "OK"
        v.save()
        return HttpResponse(status=200)
    # Redirect to home if method is anything but POST
    else:
        return HttpResponseRedirect(reverse('home'))


