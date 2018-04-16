from django.urls import path
from . import views


urlpatterns = [
    path('get', views.getalarms, name='getalarms'),
    path('datadump', views.recvdata, name='datadump'),
    path('view', views.viewalarms, name='viewalarms'),
    path('set', views.setalarms, name="setalarm")
]
