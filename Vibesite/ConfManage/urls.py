from django.urls import path, include
from ConfManage import views

urlpatterns = [
    path('<int:conf_id>/updateInfo', views.updateInfo),
    path('<int:conf_id>/dissolve', views.dissolveMeeting),
    path('<int:conf_id>/', views.meetingView, name='meeting'),
    # 下载
    path('<int:conf_id>/contribtemplate', views.contribtemplate, name='contribtemplate'),
    path('download/<str:filename>', views.download, name='download'),
]
