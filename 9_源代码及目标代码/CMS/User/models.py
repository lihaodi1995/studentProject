from django.db import models
from Meeting.models import *

# Create your models here.
class User(models.Model):
	username = models.CharField(
		max_length = 32,
		unique = True,
		)
	password = models.CharField(
		max_length = 32,
		)
	email = models.CharField(
		max_length = 32,
		null = True,
		)
	tel = models.CharField(
		max_length = 20,
		null = True,
		)
	favorite = models.ManyToManyField(Meeting, related_name = "User_set",blank = True,)
	participate = models.ManyToManyField(Meeting, related_name = "Attendee_set",blank = True,)
	