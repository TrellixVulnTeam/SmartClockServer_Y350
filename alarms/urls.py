from django.urls import path
from . import views


urlpatterns = [
    path('get/<clockid>', views.getalarms, name='getalarms'),
    path('datadump', views.recvdata, name='datadump'),
    path('view', views.viewalarms, name='viewalarms'),
    path('set', views.setalarms, name="setalarm"),
    path('delete/<apk>', views.deletealarms, name='delete'),
]
