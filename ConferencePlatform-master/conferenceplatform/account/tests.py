from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from .views import *

class SimpleTest(TestCase):
    def setUp(self):
        pass