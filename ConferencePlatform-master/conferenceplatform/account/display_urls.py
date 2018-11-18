from django.urls import path
from . import display_views

urlpatterns = [
    path('my_conference/', display_views.get_conferences_by_organization, name='my_conferences'),
    path('my_submission/', display_views.get_submissions_by_submitter, name='my_submission'),
    path('my_submission/<str:state>/', display_views.get_submissions_by_submitter, name='my_submission_state'),
    path('my_subusers/', display_views.get_subuser_by_org, name='my_subusers'),
    path('my_org_info/', display_views.get_detail_by_request_org, name='org_info'),
    path('organization/<int:id>/', display_views.get_images_by_org, name='organization_info'),
    path('conference/<int:id>/papers/', display_views.get_papers_by_conference, name='conference_papers'),
    path('conference/<int:id>/activities/', display_views.get_activities_by_conference, name='conference_activities'),
    path('conference/<int:id>/registrations/', display_views.get_registrations_by_conference, name='conference_registrations'),
    path('test/', display_views.test1, name='test')
]