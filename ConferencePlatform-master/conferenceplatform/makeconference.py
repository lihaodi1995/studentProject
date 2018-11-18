import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conferenceplatform.settings") 

import django
django.setup()

from django.test import Client
from datetime import datetime, timedelta
from random import random, randrange
from conference.models import Subject
import json

ORG_NAME = 'test@qq.com'
ORG_PASSWORD = '123'
FILE_PATH = '/home/elin/more.txt'



title_repository = [
    '经济', '养猪', '医药', '高速', '计算机', '北京',
]
TITLE_NUM = len(title_repository)
title = title_repository[randrange(0,TITLE_NUM)] + title_repository[randrange(0,TITLE_NUM)]

subject_set = Subject.objects.all()
subject = subject_set[randrange(0,len(subject_set))].name

accept_due = datetime.now() + timedelta(hours = 1)
modify_due = accept_due + timedelta(hours = 1)
register_start = modify_due + timedelta(hours = 1)
register_due = register_start + timedelta(hours = 1)
conference_start = register_due + timedelta(hours = 1)
conference_due = conference_start + timedelta(hours = 1)
paper_template = open(FILE_PATH, 'rb')
activities = [
    {
        'start_time' : conference_start.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time' : conference_due.strftime('%Y-%m-%d %H:%M:%S'),
        'place' : 'place',
        'activity' : 'activity',
    }
]

activities = json.dumps(activities)

if __name__ == '__main__':
    c = Client()
    c.login(username=ORG_NAME, password=ORG_PASSWORD)
    response = c.post(
        '/conference/add_conference/',
        {
            'title' : title,
            'subject' : subject,
            'introduction' : 'introduction',
            'soliciting_requirement' : 'soliciting_requirement',
            'register_requirement' : 'register_requirement',
            'accept_due' : accept_due,
            'register_start' : register_start,
            'register_due' : register_due,
            'conference_start' : conference_start,
            'conference_due' : conference_due,
            'paper_template' : paper_template,
            'activities' : activities,
            'template_no' : 1,
            'venue' : 'venue',
            'modify_due' : modify_due,
        }
    )
    print(response.content)
    print('title: ', title)
    print('subject: ', subject)
