from django.urls import path, include
from ContribManage import views

urlpatterns = [
    path('<int:contribution_id>/record', views.result, name='result'),
]