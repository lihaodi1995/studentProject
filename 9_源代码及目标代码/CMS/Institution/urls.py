from rest_framework import routers
from django.conf.urls import url, include
from .views import InstitutionViewSet,EmployeeViewSet

router = routers.DefaultRouter()
router.register('institution', InstitutionViewSet)
router.register('employee', EmployeeViewSet)
urlpatterns = router.urls 
