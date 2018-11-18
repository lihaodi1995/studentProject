from django.db import models
from Meeting.models import Meeting 
from Paper.models import Paper
# Create your models here.
class Institution(models.Model):
	id=models.AutoField(
		primary_key = True,
		)
	name=models.CharField(
		max_length=128,
		null=True,
		)
	corporate_id=models.CharField(
		max_length=256,
		null=True,
		)
	establish_date=models.DateField(
		null=True,
		)
	place=models.CharField(
		max_length=256,
		null=True,
		)
	legal_person=models.CharField(
		max_length=256,
		null=True,
		)
	type=models.CharField(
		max_length=16,
		null=True,
		)
	status=models.CharField(
		max_length=16,
		null=True,
		)
	

class Employee(models.Model):
	id=models.AutoField(
		primary_key=True,
		)
	username=models.CharField(
		null=True,
		max_length=256,
		)
	password=models.CharField(
		null=True,
		max_length=256,
		)
	email=models.CharField(
		null=True,
		max_length=256,
		)
	tel=models.CharField(
		null=True,
		max_length=20,
		)
	institution=models.ForeignKey(
		'Institution',
		on_delete=models.CASCADE,
		default = "",
		)