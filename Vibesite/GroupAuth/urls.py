from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:group_id>/create',views.createMeeting),
    path('<int:group_id>/updateInfo', views.updateInfo),
    path('<int:group_id>/dissolve', views.dissolveGroup),
    path('<int:group_id>/',views.groupView,name='group'),
    path('meeting/add',views.addMeeting),
    path('<int:group_id>/addMember',views.addMember),
    path('create',views.createGroupIndex),
    path('api/add',views.createGroup),
    path('<int:group_id>/kickMember',views.kickMember),
    path('<int:group_id>/changeAdmin',views.changeAdmin),
    path('checklist',views.checkAuthorization),
    path('authorization/<int:authorization_id>/info',views.authorizationInfo),
    path('authorization/<int:authorization_id>/record',views.authorizationRecord),
]