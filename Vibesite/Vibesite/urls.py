"""Vibesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.views.generic.base import RedirectView
from django.urls import include, path
from django.conf.urls import include,url
from UserAuth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('testbase/', include('testroot.urls')),
    #url(r'^index/',views.index),
    url(r'^login/',views.login),
    url(r'^register/',views.register),
    url(r'^logout/',views.logout),
    url(r'^userinfo/',views.userinfo),
    url(r'^infoedit/',views.infoedit),
    path('meeting/', include('ConfManage.urls')),
    path('group/', include('GroupAuth.urls')),
    path('contrib/', include('UserContrib.urls')),
    path('contribution/', include('ContribManage.urls')),
    path('usercontrib/',include(('UserContrib.urls','UserContrib'), namespace='UserContrib')),
    path('', RedirectView.as_view(url="/index/")),
    url(r'^UserContrib/', include('UserContrib.urls')),
    path('index/', include(('UserFunction.urls','UserFunction'),namespace='UserFunction')),
]