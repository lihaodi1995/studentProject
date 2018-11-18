from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.extremly_complicate_search, name='search'),
]