from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('change_password/', views.change_password, name='change_password'),
    path('normal_user_register/', views.normal_user_register, name='normal_user_register'),
    path('organization_user_register/', views.organization_user_register, name='organization_user_register'),
    path('organization_sub_user_register/', views.organization_sub_user_register, name='organization_sub_user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_type/', views.user_type, name='user_type'),
    path('delete_sub_user/', views.delete_sub_user, name='delete_sub_user'),
    path('csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('username/', views.get_username, name='get_username'),
    path('upload_pic/', views.upload_pic, name='upload_pic'),
    path('collect/<int:pk>/', views.collect, name='collect'),
    path('discollect/<int:pk>/', views.discollect, name='discollect'),
    path('collect_list/', views.collect_list, name='collect_list'),
    path('is_collected/<int:pk>/', views.is_collected, name='is_collected'),
    path('random_6_orgs/', views.random_6_orgs, name='random_6_orgs'),
    path('test_email/', views.test_email, name='test_email'),
    path('process_org/', views.process_orgnization_register, name='process_orgnization_register'),
    path('process_org_list/', views.process_org_list, name='process_org_list'),
]