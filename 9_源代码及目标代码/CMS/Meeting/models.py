# Create your models here.
from django.db import models
import django.utils.timezone as timezone
from Institution.models import *

class Meeting(models.Model):
	meeting_id = models.AutoField(
		primary_key = True,
		)
	title = models.CharField(
		max_length = 128,
		null = True,
		)
	intro = models.CharField(
		max_length = 512,
		null = True,
		)
	essay_request = models.CharField(
		max_length = 512,
		null=True,
		)
	ddl_date = models.DateTimeField(	#截稿日期
		null=True,
		)
	result_notice_date = models.DateTimeField(	#录用通知日期
		null=True,
		)
	regist_attend_date = models.DateTimeField(	#用户注册参加会议截止日期
		null=True,
		)
	meeting_date = models.DateTimeField(	#会议开始日期
		null=True,
		)
	meeting_end_date = models.DateTimeField(	#会议开始日期
		null=True,
		)
	schedule = models.CharField(
		max_length = 128,
		null=True,
		)
	organization = models.CharField( #组织机构
		max_length = 128,
		null = True,
		)
	template = models.CharField( 	#论文模板url
		max_length = 64,
		null = True,
		)
	receipt	= models.FloatField(		#pdf或jpg(url)
		null = True,
		)
	support = models.CharField(		#住宿交通
		max_length = 128,
		null = True,
		)
	about_us = models.CharField(
		max_length = 128,
		null = True,
		)
	institution = models.ForeignKey(
		'Institution.Institution',
		on_delete=models.CASCADE,
		default = "",
		)