from django.utils import timezone
from enum import Enum
from .models import *
import datetime
import os
from conferenceplatform.settings import MEDIA_ROOT, MEDIA_URL

class ConferenceStatus(Enum):
    not_started = 1
    accepting_submission = 2
    reviewing_accepting_modification = 3
    reviewing = 4 # 结束接受修改后和开始会议注册前
    accepting_register = 5
    register_ended = 6
    meeting = 7
    over = 8 # 


def get_organization(user):
    if user.has_perm('account.OrganizationUser_Permission'):
        return user.organizationuser
    elif user.has_perm('account.OrganizationSubUser_Permission'):
        return user.organizationsubuser.organization
    else:
        return None

def valid_timepoints(conf):
    res =  (conf.accept_start < conf.accept_due 
        and conf.register_start < conf.register_due
        and conf.register_due < conf.conference_start
        and conf.conference_start < conf.conference_due)
    if conf.modify_due != None:
        res = (res and conf.accept_due < conf.modify_due 
                and conf.modify_due < conf.register_start)
    return res

def conference_status(conf):
    now = datetime.datetime.now()
    if now < conf.accept_start:
        return ConferenceStatus.not_started
    elif now < conf.accept_due:
        return ConferenceStatus.accepting_submission
    elif now < conf.register_start:
        if conf.modify_due == None:
            return ConferenceStatus.reviewing_accepting_modification
        else:
            if now < conf.modify_due:
                return ConferenceStatus.reviewing_accepting_modification
            else:                
                return ConferenceStatus.reviewing     
        # now >= conf.accept_due, 已经结束接受投稿
        # 如果这时 modify_due没有设置，那么进入状态 modification_due_not_given
        # 直到 modify_due 被设置
    elif now < conf.register_due:
        return ConferenceStatus.accepting_register
    elif now < conf.conference_start:
        return ConferenceStatus.register_ended
    elif now < conf.conference_due:
        return ConferenceStatus.meeting
    else:
        return ConferenceStatus.over

def add_activity(conference, act_json):    
     Activity.objects.create(
         conference=conference,
         start_time=act_json['start_time'],
         end_time=act_json['end_time'],
         place=act_json['place'],
         activity=act_json['activity'],
     )


def edit_activity(pk, act_json):
     Activity.objects.filter(pk=pk).update(
         start_time=act_json['start_time'],
         end_time=act_json['end_time'],
         place=act_json['place'],
         activity=act_json['activity'],
     )

def get_sheet_value_from_state(sub_state):
    d = {
        'S': '待审核',
        'P': '审核通过',
        'M': '需要修改',
        'R': '拒稿',
    }
    return d[sub_state]

def export_path(conf_id, filename):
    d = os.path.join(MEDIA_ROOT, 'conference_'+str(conf_id)+'/exports/')
    if not os.path.exists(d):
        os.makedirs(d, 0o775)
    return os.path.join(d, filename)

def export_url(conf_id, filename):
    d = os.path.join(MEDIA_URL, 'conference_'+str(conf_id)+'/exports/')
    return os.path.join(d, filename)