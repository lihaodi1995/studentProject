from rest_framework import routers
from django.conf.urls import url, include
from Admin.views import *
router = routers.DefaultRouter()
router.register('', AdminViewSet)

urlpatterns = router.urls