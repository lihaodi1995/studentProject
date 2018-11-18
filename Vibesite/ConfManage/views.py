# Create your views here.
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from UserAuth.models import User
from UserContrib.views import *
from UserContrib.models import Contribution
from .models import Conference,ConferenceRegistration,RegisteredUser
from UserAuth.models import User
from UserFunction.models import *

from django.http import StreamingHttpResponse
from django.template.response import TemplateResponse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect

from django.template import loader

from utils import sendmail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.conf import settings

import os
import threading
import time

class email_queue():

    REGITSTER_DATE_END,SUBMIT_DATE_END,MODIFY_DATE_END,CONFERENCE_DATE = range(4)

    def __init__(self):
        pass

    def push(self,conf_id,time,phase):
        now = timezone.now()
        if now < time + timedelta(days=-1):
            try:
                message = PushMessages.objects.get(conference_id=conf_id,phase=phase)
            except Exception as e:
               message = PushMessages()
                 
            message.conference_id = conf_id
            message.time = time
            message.phase = phase
            message.save()

    def pushconf(self,conference):
        conf_id = conference.conf_id
        self.push(conf_id,conference.register_date_end,self.REGITSTER_DATE_END)
        self.push(conf_id,conference.submit_date_end,self.SUBMIT_DATE_END)
        self.push(conf_id,conference.modify_date_end,self.MODIFY_DATE_END)
        self.push(conf_id,conference.conference_date,self.CONFERENCE_DATE)

    def peek(self):
        try:
            messages = PushMessages.objects.order_by('time')
            if len(messages) > 0:
                return messages[0]
            else:
                return None
        except Exception as e:
            return None
       
    def send_email(self):
        while True:
            message = self.peek()
            if not message is None:
                now = timezone.now()
                if now >= message.time + timedelta(days=-1):
                    conference_id = message.conference_id
                    bookmarks = Bookmark.objects.filter(conference_id = conference_id)
                    users = []
                    for bookmark in bookmarks:
                        users.append(User.objects.get(user_id=bookmark.user_id))
                    user_emails = []
                    for user in users:
                        user_emails.append(user.email)

                    conference = Conference.objects.get(conf_id=conference_id)
                    content = None
                    if message.phase == self.REGITSTER_DATE_END:
                        content = '%s的注册日期(%s)快要到啦'%(conference.title,conference.register_date_end)
                    if message.phase == self.SUBMIT_DATE_END:
                        content = '%s的第一次投稿日期(%s)快要到啦'%(conference.title,conference.submit_date_end)
                    if message.phase == self.MODIFY_DATE_END:
                        content = '%s的第二次投稿日期(%s)快要到啦'%(conference.title,conference.modify_date_end)
                    if message.phase == self.CONFERENCE_DATE:
                        content = '%s的开始日期(%s)快要到啦'%(conference.title,conference.conference_date)
                    try:
                        message.delete()
                        sendmail.sendmail(user_emails,'会议管理系统通知邮件',content)
                    except Exception as e:
                        print(e)
                else:
                    break
            else:
                break

def sendmymail():
    queue = email_queue()
    while True:
        queue.send_email()
        print("send email")
        time.sleep(60)
thread = threading.Thread(target=sendmymail)
thread.setDaemon(True)
thread.start()
  
if not os.path.exists(r'./saved_files'):
    os.mkdir(r'./saved_files')
SAVED_FILES_DIR=r'./saved_files'

queue = email_queue()

#修改会议
@csrf_exempt
@require_http_methods(["POST"])
def updateInfo(request, conf_id):

    try:
        pass
    except Exception as e:
        raise e
    request.session['meeting_label'] = 'meetinginfo'

    # 未登陆不允许访问
    if not request.session.get('is_login'):
        return HttpResponse("禁止修改")
    
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    meeting = Conference.objects.get(conf_id=conf_id)

    # 不属于同一组不允许访问
    if user.group_id != meeting.group_id:
        return HttpResponse("禁止修改")

    try:
        type = request.POST.get('type')
        value = request.POST.get('value')
        
        meeting = Conference.objects.get(conf_id=conf_id)
        if type == '1' :
            meeting.title = value
        elif type == '2':
            meeting.introduction = value
        elif type == '3':
            meeting.submit_date_start = value
        elif type == '4':
            meeting.submit_date_end = value
        elif type == '5':
            meeting.modify_date_start = value
        elif type == '6':
            meeting.modify_date_end = value
        elif type == '7':
            meeting.register_date_start = value
        elif type == '8':
            meeting.register_date_end = value
        elif type == '9':
            meeting.conference_date = value
        elif type == '10':
            meeting.arrangement = value
        elif type == '11':
            meeting.fee = value
        elif type == '12':
            meeting.logistics = value
        elif type == '13':
            meeting.contact = value
        meeting.save()
        meeting = Conference.objects.get(conf_id=conf_id)
        queue.pushconf(meeting)
        res = HttpResponse("修改成功")
    except Exception as e:
        print(e)
        res = HttpResponse("修改失败")
    return res

@csrf_exempt
@require_http_methods(["GET"])
def dissolveMeeting(request, conf_id):
    #未登陆不允许访问
    try:
        conference = Conference.objects.get(conf_id=conf_id)
    except Exception as e:
        return HttpResponseRedirect('error.html')
    if not request.session.get('is_login'):
        return redirect('/index/')   
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    meeting = Conference.objects.get(conf_id=conf_id)
    #不属于同一组不允许访问
    if user.group_id != meeting.group_id:
        return redirect('/index/')

    try:
        contribs = list(Contribution.objects.filter(conference_id=meeting.conf_id))
        registers = list(ConferenceRegistration.objects.filter(conf_which_id=meeting.conf_id))
        for x in registers:
            x.delete()
        for x in contribs:
            x.delete()
        meeting.delete()
    except Exception as e:
        print(e)
        return HttpResponse("解散失败")
    return HttpResponse("解散成功")

def meetingView(request,conf_id):

    #未登陆不允许访问
    label = 'meetinginfo'
    if not request.session.get('is_login'):
        return redirect('/index/')

    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    meeting = Conference.objects.get(conf_id=conf_id)

    #不属于同一组不允许访问
    if user.group_id != meeting.group_id:
        return redirect('/index/')

    if not request.session.get('group_label') is None:
        request.session["group_label"] = None

    label = 'meetinginfo'
    if not request.session.get('meeting_label') is None:
        label = request.session['meeting_label']

    contributions = meeting.contribution_set.filter(register_status=0)
    reg_contributions = Contribution.objects.filter(conference_id=conf_id,register_status=1)
    template = loader.get_template('meeting/meeting.html')
    part_people = ConferenceRegistration.objects.filter(conf_which_id=conf_id)
    id_list = list()
    for p in part_people:
        if p.user_who_paid not in id_list:
            id_list.append(p.user_who_paid)
            u = User.objects.get(user_id = p.user_who_paid)
            p.name = u.user_name          

    context = {
        'meeting':meeting,
        'contributions': contributions,
        'reg_contributions':reg_contributions,
        'part_people':part_people,
        'label':label,
    }
    return TemplateResponse(request,template,context)

@csrf_exempt
@require_http_methods(["POST"])
def contribtemplate(request, conf_id):

    request.session['meeting_label'] = 'meetinginfo'

    # 未登陆不允许访问
    if not request.session.get('is_login'):
        return redirect('/index/')
    
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    meeting = Conference.objects.get(conf_id=conf_id)

    # 不属于同一组不允许访问
    if user.group_id != meeting.group_id:
        return redirect('/index/')

    try:
        file = request.FILES.get('file',None)
        filename=time.strftime("%Y%m%d%H%M%S", time.localtime())+str(user_id)+"."+file.name.split('.')[-1]
        pathname = os.path.join(settings.CONTRIBUTION_TEMPLATE_DIR, filename)
        UPLOAD(file,pathname)
        
        meeting.template = filename
        meeting.save()
        
        res = HttpResponse("修改成功")
    except Exception as e:
        print(e)
        res = HttpResponse("修改失败")
    return res

def download(request, filename):
    if not request.session.get('user_id'):
        redirect('/login/')

    the_file_name = os.path.join(settings.SAVED_CERTIFICATE_DIR,filename)  # 要下载的文件路径
    response = StreamingHttpResponse(readFile(the_file_name))
    response['Content-Type'] = 'image/png'
    response['Content-Disposition'] = 'inline;filename=%s' % filename
    return response

def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break
@csrf_exempt
@require_http_methods(["POST"])
def contribtemplate(request, conf_id):

    request.session['meeting_label'] = 'meetinginfo'

    # 未登陆不允许访问
    if not request.session.get('is_login'):
        return redirect('/index/')
    
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    meeting = Conference.objects.get(conf_id=conf_id)

    # 不属于同一组不允许访问
    if user.group_id != meeting.group_id:
        return redirect('/index/')

    try:
        file = request.FILES.get('file',None)
        filename=time.strftime("%Y%m%d%H%M%S", time.localtime())+str(user_id)+"."+file.name.split('.')[-1]
        pathname = os.path.join(settings.CONTRIBUTION_TEMPLATE_DIR, filename)
        UPLOAD(file,pathname)
        
        meeting.template = filename
        meeting.save()
        
        res = HttpResponse("修改成功")
    except Exception as e:
        print(e)
        res = HttpResponse("修改失败")
    return res
