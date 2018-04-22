from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


# Link account with clock
def link(request):
    if request.method == "POST" and request.user.is_authenticated:
        if request.POST.get("cID"):
            request.user.profile.clock = request.POST.get("cID")
            request.user.profile.save()
            print(request.user.profile.clock)
            return HttpResponseRedirect(reverse('home'))
