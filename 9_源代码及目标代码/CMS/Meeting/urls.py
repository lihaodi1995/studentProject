from rest_framework import routers
from django.conf.urls import url, include
from Meeting.views import *
router = routers.DefaultRouter()
router.register('', MeetingViewSet)

urlpatterns = router.urls
