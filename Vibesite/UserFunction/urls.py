from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:conf_id>', views.confDetail),
    path('search/', views.search, name = 'search'),
    path('subscribedlist/',views.view_subscribed,name='subscribedlist'),
]