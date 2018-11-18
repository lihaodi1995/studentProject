# Create your views here.
import time
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.template.response import TemplateResponse
from django.template import loader
from django.shortcuts import redirect

from ConfManage.models import Conference,ConferenceRegistration,RegisteredUser
from UserAuth.models import User
from GroupAuth.models import Group,Authorization
from UserContrib.models import Contribution

from UserAuth.models import User
from django.contrib import messages
from django.utils import timezone
from utils import sendmail

from ConfManage.views import *
from UserContrib.views import *
import threading
import traceback
import os
from django.conf import settings
queue = email_queue()

def isGroupMember(user_id,group_id):
    user = User.objects.get(user_id = user_id)
    #import pdb; pdb.set_trace()
    group = Group.objects.get(group_id=group_id)
    if group.group_auth.status !='g':
        return False
    if user.group_id != group_id:
        return False
    return True

#创建会议页面
def createMeeting(request,group_id):
    user_id = request.session['user_id']
    result = isGroupMember(user_id,group_id)
    if not result:
        return redirect('/index/')
    #不是组成员不允许访问
    template = loader.get_template('group/create_meeting.html')
    context = {
        'group_id':group_id
    }
    return TemplateResponse(request,template,context)

#添加组成员
@csrf_exempt
@require_http_methods(["POST"])
def addMember(request,group_id):
    try:
        email = request.POST.get('email')
        request.session['group_label'] = 'members'
        try:
            user = User.objects.get(email = email)
        except:
            res = HttpResponse("用户不存在")
            return res

        if not user.group_id:
            user.group_id = group_id
            user.save()
            res = HttpResponse("添加成功")
        elif user.group_id == group_id:
            res = HttpResponse("用户已是成员")
        else:
            res = HttpResponse("用户已加入其他组")
    except:
        res = HttpResponse("添加失败")
    return res

#踢组成员
@csrf_exempt
@require_http_methods(["POST"])
def kickMember(request,group_id):
    try:
        user_id = request.POST.get('user_id')
        request.session['group_label'] = 'members'
        try:
            user = User.objects.get(user_id = user_id)
        except:
            res = HttpResponse("用户不存在")
            return res

        user.group_id = None
        user.save()         
        res = HttpResponse("移除成功")
    except:
        res = HttpResponse("移除失败")
    return res

#转让管理员
@csrf_exempt
@require_http_methods(["POST"])
def changeAdmin(request,group_id):
    try:
        admin_id = request.POST.get('admin_id')
        user_id = request.POST.get('user_id')
        request.session['group_label'] = 'members'
        try:
            admin = User.objects.get(user_id = admin_id)
            user = User.objects.get(user_id = user_id)
            group = Group.objects.get(group_id = group_id)
        except Exception as e:
            print(e)
            res = HttpResponse("转让失败")
            return res

        group.admin = user_id
        group.save()
        res = HttpResponse("转让成功")
        
    except:
        res = HttpResponse("转让失败")
    return res

#创建会议
def addMeeting(request):
    group_id = request.POST.get('group_id')
    #import pdb; pdb.set_trace()
    try:
        conference = Conference()
        conference.title = request.POST.get('title')
        conference.introduction = request.POST.get('introduction')
        conference.register_date_end = request.POST.get('register_date_end')
        conference.register_date_start = request.POST.get('register_date_start')
        conference.submit_date_start = request.POST.get('submit_date_start')
        conference.submit_date_end = request.POST.get('submit_date_end')
        conference.modify_date_start = request.POST.get('modify_date_start')
        conference.modify_date_end = request.POST.get('modify_date_end')
        conference.conference_date = request.POST.get('conference_date')
        conference.logistics = request.POST.get('logistics')
        conference.contact = request.POST.get('contact')
        conference.fee  = request.POST.get('fee')
        conference.arrangement = request.POST.get('arrangement')
        conference.inform_date=request.POST.get('inform_date')

        # 上传论文模板，求求你解决冲突的时候看一眼，不要再删了！！！
        file=request.FILES.get('template',None)
        filename = time.strftime("%Y%m%d%H%M%S", time.localtime()) + str(request.session['user_id']) + "." + file.name.split('.')[-1]
        pathname = os.path.join(settings.CONTRIBUTION_TEMPLATE_DIR, filename)
        UPLOAD(file,pathname)
        conference.template = filename

        conference.group_id = group_id
        conference.save()
        conference = Conference.objects.order_by('-conf_id')[0]
        queue.pushconf(conference)
        messages.success(request,'创建会议成功')
    except Exception as e:
        print(e)
        messages.success(request,'创建会议失败')
    return HttpResponseRedirect('/group/%s'% group_id)

#修改组信息
@csrf_exempt
@require_http_methods(["POST"])
def updateInfo(request, group_id):
    # 未登陆不允许访问
    if not request.session.get('is_login'):
        return HttpResponse("禁止修改")
    
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    if not user.group_id == group_id:
        return HttpResponse("禁止修改")

    request.session['group_label'] = 'groupinfo'
    try:
        type = request.POST.get('type')
        value = request.POST.get('value')
        group = Group.objects.get(group_id=group_id)
        if type == '1':
            group.group_name = value
        elif type == '2':
            group.admin = value
        group.save()
        res =HttpResponse("修改成功")
        
    except:
        res = HttpResponse("修改失败")
    return res

#解散组织
@csrf_exempt
@require_http_methods(["GET"])
def dissolveGroup(request, group_id):
    #未登陆不允许访问
    if not request.session.get('is_login'):
        return redirect('/index/')
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    group = Group.objects.get(group_id=group_id)
    #不是组成员不允许访问
    if user.group_id != group_id:
        return redirect('/index/')
    # 删除所有相关信息
    try:
        group = Group.objects.get(group_id=group_id)
        auth = group.group_auth
        confs = list(Conference.objects.filter(group_id=group_id))
        contribs = []
        registers = []
        register_users = []
        for conf in confs:
            contribs.extend(list(Contribution.objects.filter(conference_id=conf.conf_id)))
            registers.extend(list(ConferenceRegistration.objects.filter(conf_which_id=conf.conf_id)))   
        for x in registers:
            x.delete()
        for x in contribs:
            x.delete()
        for x in confs:
            x.delete()
        group.delete()
        auth.delete()
    except Exception as e:
        print(e)
        return HttpResponse("解散失败")
    return HttpResponse("解散成功")

#组织管理界面
def groupView(request,group_id):

    label = 'groupinfo'
    if not request.session.get('group_label') is None:
        label = request.session['group_label']

    if not request.session.get('meeting_label') is None:
        request.session['meeting_label'] = None

    #未登陆不允许访问
    if not request.session.get('is_login'):
        return redirect('/index/')

    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    group = Group.objects.get(group_id=group_id)

    #不是组成员不允许访问
    if user.group_id != group_id:
        return redirect('/index/')
    # 未审核组禁止进入组主页
    if not group.group_auth.status == "g":
        return HttpResponse('<script>alert("该组还未通过审核！");location.href="/index/";</script>')
    
    members = group.user_set.all()
    template = loader.get_template('group/group.html')
    meetings = group.conference_set.all()

    for meeting in meetings:
        getMeetingState(meeting)
    
    admin = User.objects.get(user_id = group.admin)
    group.admin_name = admin.user_name

    context = {
        'group':group,
        'members': members,
        'list_data':meetings,
        'admin':admin,
        'user_id':user_id,
        'label':label,
    }

    return TemplateResponse(request,template,context)

def getMeetingState(meeting):
    now = timezone.now()
    if now < meeting.submit_date_start:
        print(meeting.submit_date_start)
        meeting.state = '暂不可投稿'
    elif now < meeting.submit_date_end:
        meeting.state = "初稿投稿中"
    elif now < meeting.modify_date_start:
        meeting.state = "初稿投稿截止"
    elif now < meeting.modify_date_end:
        meeting.state = "修改稿投稿中"
    elif now < meeting.register_date_start:
        meeting.state = "修改稿投稿截止"
    elif now < meeting.register_date_end:
        meeting.state = "注册中"
    elif now < meeting.conference_date:
        meeting.state = "注册截止"
    else:
        meeting.state = "已经举办"

#返回组织认证界面
def createGroupIndex(request):
    if not request.session.get('is_login'):
        return redirect('/index/')
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    # 已经拥有组的成员不允许访问
    if user.group_id is not None:
        return redirect('/index/')
    template = loader.get_template('group/create_group.html')
    return TemplateResponse(request,template,{})


@require_http_methods(['POST'])
def createGroup(request): 
    if not request.session.get('is_login'):
        return redirect('/index/')
    user_id = request.session['user_id']
    user = User.objects.get(user_id = user_id)
    # 已经拥有组的成员不允许访问
    if user.group_id is not None:
        return redirect('/index/')

    try: 
        group = Group(request.POST)
        
        data = dict(request.POST)
        # 获取对应信息
        auth_field = [field.name for field in Authorization._meta.fields]
        group_field = [field.name for field in Group._meta.fields]
        auth_dict = {x:y[0] for x,y in data.items() if x in auth_field}
        group_dict = {x:y[0] for x,y in data.items() if x in group_field}
        # 处理认证文件
        file = request.FILES.get('cert_file')  
        file_url = os.path.join('./static/auth',str(int(time.time()))+file.name)
        print(file_url)
        with open(file_url,'wb') as f:
            f.write(file.read())
        # 创建认证信息
        auth = Authorization(**auth_dict)  
        auth.cert_url = file_url[1:]  # 文件的存储位置
        auth.save()
        # 创建用户组信息
        group = Group(**group_dict)
        group.group_auth = auth
        group.admin = request.session['user_id']
        group.save()
        # 更改用户的group_id
        user = User.objects.get(pk=group.admin)
        user.group = group
        user.save()
        res = HttpResponse('<script>alert("上传成功,请等待邮件通知。");location.href="/index/"</script>')
    except Exception as e:
        print(e)
        res = HttpResponse('<script>alert("上传失败")</script>')
    return res
    
def authorizeView(request):
    template = loader.get_template('group/authorize.html')
    context = {}
    return TemplateResponse(request,template,context)


#审核组织认证信息
def checkAuthorization(request):
    template = loader.get_template('group/checklist.html')
    authorizations = Authorization.objects.filter(status = 'p')
    context = {
       'authorizations':authorizations
    }
    return TemplateResponse(request,template,context)

def authorizationInfo(request,authorization_id):
    template = loader.get_template('group/authorization_info.html')
    authorization = Authorization.objects.get(authorization_id = authorization_id)
    context = {
        'authorization':authorization
    }
    return TemplateResponse(request,template,context)

@csrf_exempt
@require_http_methods(["POST"])
def authorizationRecord(request,authorization_id):
    try:
        re = request.POST.get('re')
        authorization = Authorization.objects.get(authorization_id=authorization_id)
        authorization.status = re
        group = Group.objects.get(group_auth_id = authorization.authorization_id)
        admin = User.objects.get(user_id = group.admin)
        if re == 'g':
            content = '你的组织认证信息的审核结果为通过认证'
            authorization.save()
        elif re=='r':
            content = '你的组织认证信息的审核结果为不通过认证'
            group.delete()
            authorization.delete()
        #import pdb; pdb.set_trace()
        res =HttpResponse("审核成功")
        thread_new = myThread(1,admin.email,'会议管理系统通知邮件', content) 
        thread_new.start()
    except:
        traceback.print_exc()
        res = HttpResponse("审核失败")
    return res

class myThread(threading.Thread):
    def __init__(self,threadID,email,message,html):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.email = email
        self.message = message
        self.html = html
    def run(self):
        sendmail.sendmail([self.email], self.message, self.html)

if not os.path.exists('./static/auth'):
    os.mkdir('./static/auth')
