from rest_framework import routers
from django.conf.urls import url, include
from User.views import *
router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = router.urls