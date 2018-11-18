from django.db import models
from User.models import *
from Meeting.models import *

# Create your models here.
class Paper(models.Model):
	author_1 = models.CharField(
		max_length = 20,
		null = False,
		)
	author_2 = models.CharField(
		max_length = 20,
		null = True,
		)
	author_3 = models.CharField(
		max_length = 20,
		null = True,
		)
	title = models.CharField(
		max_length = 64,
		)
	abstract = models.CharField(
		max_length = 1024,
		null = True,
		)
	keyword = models.CharField(
		max_length = 128,
		null = True,
		)
	content = models.FileField(
		upload_to='paper/'
		)
	status = models.IntegerField(
		null = False,
		)
	owner = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default = "",
		)
	meeting = models.ForeignKey(
		Meeting,
		on_delete=models.CASCADE,
		default = "",
		)

