from django import forms
from django.db import IntegrityError
from .models import *
from conference.models import *
import jieba

def get_chunks(str):
    cleaner = forms.CharField(required=False)
    ret = []
    for chunk in jieba.cut(str):
        c = cleaner.clean(chunk)
        if len(c) > 0 and len(c) <= 64:
            ret.append(c)
    return ret

def do_segmentation_for_conf(conf):
    li = get_chunks(conf.title)
    for c in li:
        try:
            ent = ChunkFromConfTitle.objects.get(value=c)
            ent.conf_set.add(conf)
        except ChunkFromConfTitle.DoesNotExist:
            o = ChunkFromConfTitle.objects.create(
                value=c
            )
            o.conf_set.add(conf)

# only used when there are 
# old conferences added before we decided to do segmentation
def do_segmentation_for_all_confs():
    for conf in Conference.objects.all():
        do_segmentation_for_conf(conf)  

