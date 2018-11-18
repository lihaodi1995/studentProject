from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'UserAuth'
urlpatterns = [
    url(r'^index/',views.index),
    url(r'^login/',views.login),
    url(r'^register/',views.register),
    url(r'^logout/',views.logout),
    url(r'^userinfo/',views.user),
    url(r'^infoedit/',views.infoedit),
]