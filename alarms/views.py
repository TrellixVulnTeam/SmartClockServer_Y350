from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from json import loads, JSONDecodeError
from .models import Vector, Alarm, Profile
from .forms import AlarmForm

# TODO (optional): Automatically sync clock set alarms with server
# TODO: Finish the alarms view


# Allow the user to set new alarms
def setalarms(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = AlarmForm(request.POST)
        if form.is_valid():
            # process data
            return HttpResponseRedirect(reverse('home'))
    else:
        form = AlarmForm()
    # TODO: Set up "form" correctly
    return render(request, 'alarms/set.html', {'form': form})


# Show the user his alarms
def viewalarms(request):
    params = {}
    # Check to see if the user is logged in
    if request.user.is_authenticated:
        usr = request.user
        # Get all alarms associated with the user
        alarms = list(Alarm.objects.filter(user=usr))
        # TODO: Make this less hacky
        # Makes a list of tuples of the form:
        #   (label, date, doesrepeat, origin, destination)
        params["alarms"] = []
        for a in alarms:
            params["alarms"].append(
                (a.label,
                 a.date,
                 a.repeat,
                 a.origin,
                 a.destination)
            )
        return render(request, 'alarms/list.html', params)
    return HttpResponseRedirect(reverse('home'))


# Get a JSON of all alarms and return it
def getalarms(request):
    if request.method == 'GET':
        # Get the clock ID
        cID = request.get("clockid")
        # Get all alarms associated with the clockid/user
        usr = Profile.objects.get(clock=cID)
        alarms = list(Alarm.objects.filter(user=usr))
        # Return all alarms currently set
        return JsonResponse(alarms, safe=False)
    else:
        # An end user will always use a GET, don't need to redirect
        return HttpResponseBadRequest

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
