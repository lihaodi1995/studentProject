from django.shortcuts import render
from conference.models import *
from account.models import *
from django import forms
import jieba
from django.http.response import JsonResponse
from django.db.models import Q, F
from collections import OrderedDict
from datetime import datetime
from conference.utils import conference_status

class Search_Form(forms.Form):
    keywords = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    organization = forms.CharField(required=False)


def add_dict(conf_dict, confqueryset):
    for conf in confqueryset:
        if conf.pk in conf_dict:
            conf_dict[conf.pk] += 1
        else:
            conf_dict[conf.pk] = 1



def extremly_complicate_search(request):
    data = {'data':[]}
    form = Search_Form(request.GET)
    if form.is_valid() is False:
        return JsonResponse({'message' : 'format error'})
    keywords = form.cleaned_data['keywords']
    subject = form.cleaned_data['subject']
    organization = form.cleaned_data['organization']

    all_conf = Conference.objects.all()
    conf_dict = OrderedDict()

    if subject != '':
        all_conf = all_conf.filter(subject__name__icontains = subject)
    
    if organization != '':
        all_conf = all_conf.filter(organization__org_name__icontains = organization)
    
    if keywords != '':
        cut_keywords = list(jieba.cut(keywords))
        for word in cut_keywords:
            related_conf = all_conf.filter(
                Q(title__icontains = word) |
                Q(introduction__icontains = word)
            ).distinct()
            add_dict(conf_dict, related_conf)
        conf_dict = OrderedDict(sorted(conf_dict.items(), key=lambda x: x[1],  reverse=True))
        for conf in conf_dict:
            status = conference_status(Conference.objects.get(pk = conf)).value
            data['data'].append({'pk' : conf, 'relativity' : conf_dict[conf], 'status' : status})

    else:
        for conf in all_conf:
            status = conference_status(conf).value
            data['data'].append({'pk' : conf.pk, 'status':status})
    data['ammount'] = len(data['data'])
    return JsonResponse(data)

