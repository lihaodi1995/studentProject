from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key = True)
    user_name = models.CharField(max_length = 32)
    password = models.CharField(max_length = 32)
    email = models.EmailField(null = False, unique = True)

    group = models.ForeignKey('GroupAuth.Group', on_delete = models.SET_NULL, null = True)