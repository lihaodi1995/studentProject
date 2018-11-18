from rest_framework import routers
from django.conf.urls import url, include
from Paper.views import *
router = routers.DefaultRouter()
router.register('', PaperViewSet)

urlpatterns = router.urls