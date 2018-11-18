from django.db import models

# Create your models here.
class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key = True)
    conference = models.ForeignKey('ConfManage.Conference', on_delete = models.CASCADE, null = True)
    user = models.ForeignKey('UserAuth.User', on_delete = models.CASCADE, null = True)