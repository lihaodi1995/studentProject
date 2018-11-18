from django.db import models
from conference.models import *

class ChunkFromConfTitle(models.Model):
    value = models.CharField(max_length=64, primary_key=True)
    conf_set = models.ManyToManyField(Conference, related_name='chunk')
