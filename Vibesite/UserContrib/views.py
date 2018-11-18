from django.shortcuts import get_object_or_404,redirect
from django.views.decorators.http import require_http_methods

from django.http import StreamingHttpResponse
from django.template.response import TemplateResponse
from django.template import loader

from UserAuth.views import *

from UserAuth.models import *
from ConfManage.models import *
from .models import Contribution
from UserAuth.models import User
from django.template.response import TemplateResponse

# Create your views here.
from django.shortcuts import render
from django.template.response import TemplateResponse
from ConfManage.models import RegisteredUser,ConferenceRegistration

# Create your views here.
from django.shortcuts import render

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template import loader
from UserFunction.models import Bookmark
from .models import Contribution
from ConfManage.models import Conference
from UserAuth.views import *

from django.utils import timezone
import os
import time
import zipfile
import io
import csv
from django.conf import settings
import datetime

# Create your views here.
@require_http_methods(['GET'])
def contribInfo(request, contrib_id):
    contrib = get_object_or_404(Contribution, pk=contrib_id)
    template = loader.get_template('contributioninfo.html')
    context = {
        'contribution':contrib,
    }
    return TemplateResponse(request, template, context)

def contriblist(request,conf_id):
    if request.session.get('is_login',False):
        try:
            latest_contributions = Contribution.objects.filter(user=request.session.get('user_id', None), conference=conf_id)
        except :
            latest_contributions = None
    else:
        latest_contributions = None
    try:
        user=request.session.get('user_id',None)
        ConferenceRegistration.objects.get(user_who_paid=user,conf_which_id=conf_id)
        registered = True
    except :
        registered = False
    try:
        meeting = Conference.objects.get(pk=conf_id)
    except:
        return error(request)

    template = loader.get_template('UserContrib/contributionlist.html')
    context = {
        'registered' : registered,
        'latest_contributions' : latest_contributions,
        'meeting' : meeting,
    }
    return TemplateResponse(request,template,context)




def form(request,conf_id,contrib_id=0):
    if not request.session.get('user_id'):
        return TemplateResponse(request,'UserAuth/login.html')
    temp=loader.get_template('UserContrib/contributionform.html')
    nowTime=datetime.datetime.now()
    try:
        cstart=Conference.objects.get(conf_id=conf_id).submit_date_start
        cend = Conference.objects.get(conf_id=conf_id).submit_date_end
        mstart=Conference.objects.get(conf_id=conf_id).modify_date_start  # 原来写的submit_date_start
        mend=Conference.objects.get(conf_id=conf_id).modify_date_end
        contributeShow = True
        modifyShow = True
        if nowTime<cstart or nowTime>cend:
             contributeShow = False
        if (nowTime<mstart or nowTime>mend) and (nowTime<cstart or nowTime>cend):
             modifyShow = False
        context={
            'user_id':request.session.get('user_id'),
            'conf_id':conf_id,
            'contrib_id':contrib_id,
            'contributeShow':contributeShow,
            'modifyShow':modifyShow,
        }
        if contrib_id:
            context['contribution']=Contribution.objects.get(contribution_id=contrib_id)
    except:
        return error(request)
    return TemplateResponse(request,temp,context)



def submit(request,conf_id,contrib_id=0):
    if not request.session.get('user_id'):
        return login(request)
    post=request.POST
    _title=post['title']
    _author=';'.join(post.getlist('author'))
    _org=';'.join(post.getlist('organization'))
    _abstract=post['abstract']

    user_id=request.session['user_id']
    if not os.path.exists(settings.SAVED_FILES_DIR):
        os.makedirs(settings.SAVED_FILES_DIR)

    file=request.FILES.get('upload',None)
    filename=time.strftime("%Y%m%d%H%M%S", time.localtime())+str(user_id)+"."+file.name.split('.')[-1]
    pathname = os.path.join(settings.SAVED_FILES_DIR, filename)

    # 根据contrib_id判断第一次提交还是修改
    if contrib_id==0:
        conf=Conference.objects.get(conf_id=conf_id)
        if timezone.now() > conf.submit_date_end:
            return contriblist(request,conf_id)
        contrib=Contribution(title=_title,author=_author,organization=_org,abstract=_abstract,url=filename,last_modified=timezone.now(),
                         user=User.objects.get(user_id=user_id),conference=Conference.objects.get(conf_id=conf_id))
    else:
        conf = Conference.objects.get(conf_id=conf_id)
        if timezone.now() > conf.modify_date_end:
            return contriblist(request,conf_id)
        contrib=Contribution.objects.get(contribution_id=contrib_id)
        contrib.title=_title
        contrib.author=_author
        contrib.organization= _org
        contrib.abstract=_abstract
        contrib.url=filename
        contrib.last_modified = timezone.now()
        contrib.modified_times+=1
    contrib.save()
    with open(pathname, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return contrib_detail(request,conf_id,contrib.contribution_id)

def download(request, contrib_id):
    if not request.session.get('user_id'):
        return login(request)
    try:
        contrib=Contribution.objects.get(contribution_id=contrib_id)
    except :
        return error(request)
    the_file_name = contrib.url  # 显示在弹出对话框中的默认的下载文件名
    filename = os.path.join(settings.SAVED_FILES_DIR,the_file_name)  # 要下载的文件路径
    if not os.path.exists(filename):
        filename=settings.DEFAULT_DOWNLOAD_FILE
        the_file_name='404.pdf'
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'inline;filename=%s'%the_file_name
    return response
# 文件不存在则返回默认文件
def download2(request, contrib_id):
    if not request.session.get('user_id'):
        return login(request)
    try:
        contrib=Contribution.objects.get(contribution_id=contrib_id)
    except :
        return error(request)
    the_file_name = contrib.url  # 显示在弹出对话框中的默认的下载文件名
    filename = os.path.join(settings.SAVED_FILES_DIR,the_file_name)  # 要下载的文件路径
    if not os.path.exists(filename):
        filename=settings.DEFAULT_DOWNLOAD_FILE
        the_file_name='404.pdf'
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment;filename=%s'%the_file_name
    return response

def zipdownload(request, conf_id):
    if not request.session.get('user_id'):
        return login(request)
    try:
        conference = Conference.objects.get(conf_id=conf_id)
    except :
        return error(request)
    contributions = conference.contribution_set.all()

    
    csvfile = io.StringIO()
    csvwriter = csv.writer(csvfile,delimiter=',')
    fields = ('投稿ID','题目','作者','所属机构','摘要','论文','审核结果','评审意见')
    csvwriter.writerow(fields)
    
    imz = InMemoryZip()
    for contribution in contributions:
        row = []
        try:
            the_file_name = contribution.url  # 显示在弹出对话框中的默认的下载文件名
            filename = os.path.join(settings.SAVED_FILES_DIR,the_file_name)  # 要下载的文件路径
            fp = open(filename,'rb')

            imz.appendfp(fp,"data/"+the_file_name)
            row.append(contribution.contribution_id)
            row.append(contribution.title)
            row.append(contribution.author)
            row.append(contribution.organization)
            row.append(contribution.abstract)
            row.append(contribution.url)
            row.append(contribution.result)
            row.append(contribution.comment)
            csvwriter.writerow(row)
            
        except Exception as e:
            print(e)

    imz.appendfp(csvfile,"overview.csv")

    response = StreamingHttpResponse(readzip(imz.in_memory_zip))
    response['Content-Type'] = 'application/x-zip-compressed'
    response['Content-Disposition'] = 'attachment;filename=Contributions.zip'
    return response

def readzip(zippt,chunk_size=512):
    zippt.seek(0)
    while True:
        c = zippt.read(chunk_size)
        if c:
            yield c
        else:
            break

def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break

def contrib_detail(request,conf_id,contrib_id):
    if not request.session.get('user_id'):
        return login(request)
    try:
        detail_list = Contribution.objects.get(contribution_id=contrib_id,conference_id=conf_id)
    except:
        return error(request)
    response = TemplateResponse(request,"UserContrib/contrib_detail.html",{"detail_list":detail_list,'conf_id':conf_id,})
    return response

def listen(request,conf_id):
    try:
        user=request.session.get('user_id',None)
        ConferenceRegistration.objects.get(user_who_paid=user,conf_which_id=conf_id)
        return contriblist(request,conf_id)
    except :
        pass
    if not request.session.get('user_id'):
        return login(request)
    template = loader.get_template('UserContrib/conferenceregister.html')
    nowTime=datetime.datetime.now()
    try:
        start=Conference.objects.get(conf_id=conf_id).register_date_start
        end = Conference.objects.get(conf_id=conf_id).register_date_end
    except:
        return error(request)
    flag = True
    if nowTime<start or nowTime>end:
        flag = False
    context={
        'conf_id':conf_id,
        'contrib_id':0,
        'showform':flag,
    }
    return TemplateResponse(request,template,context)

def paper_register(request,conf_id,contrib_id):
    if not request.session.get('user_id'):
        return login(request)
    try:
        if Contribution.objects.get(contribution_id=contrib_id).register_status:
            return contriblist(request,conf_id)
        template = loader.get_template('UserContrib/conferenceregister.html')
        nowTime=datetime.datetime.now()
        start=Conference.objects.get(conf_id=conf_id).register_date_start
        end = Conference.objects.get(conf_id=conf_id).register_date_end
    except:
        return error(request)
    flag = True
    if nowTime<start or nowTime>end:
        flag = False
    context={
        'conf_id':conf_id,
        'contrib_id':contrib_id,
        'title':Contribution.objects.get(contribution_id=contrib_id).title,
        'showform':flag,
    }
    return TemplateResponse(request,template,context)



def register_into_conference(request,conf_id,contrib_id=0):
    if not request.session.get('user_id'):
        return login(request)
    #录入付费凭证
    user_id=request.session['user_id']
    if not os.path.exists(settings.SAVED_CERTIFICATE_DIR):
        os.makedirs(settings.SAVED_CERTIFICATE_DIR)

    file = request.FILES.get('upload',None)
    filename = time.strftime("%Y%m%d%H%M%S", time.localtime())+str(user_id)+"consumn."+file.name.split('.')[-1]
    pathname = os.path.join(settings.SAVED_CERTIFICATE_DIR, filename)

    with open(pathname, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    user = request.session.get('user_id')
    if not contrib_id == 0:
        #建立注册记录
        cs = ConferenceRegistration(type = 'p',payment = filename,result = 'g',user_who_paid=user,conf_which_id=conf_id)
        cs.save()
        #修改论文注册状态
        try:
            con = Contribution.objects.get(contribution_id=contrib_id)
        except:
            return error(request)
        con.register_status = True
        con.contib_reg = cs
        con.save()
    else:
        #建立注册记录
        cs = ConferenceRegistration(type = 'a',payment = filename,result = 'g',user_who_paid=user,conf_which_id=conf_id)
        cs.save()

    #录入注册人员
    querysetlist = []
    post=request.POST
    for index in range(1,1+int(post['id'])):
        if(index % 4 == 1):
            _name=post[str(index)]
            print(_name)
        elif(index % 4 == 2):
            _gender=post[str(index)]
            print(_gender)
        elif(index % 4 == 3):
            _contact=post[str(index)]
            print(_contact)
        elif(index % 4 == 0):
            if(post[str(index)]=='True'):
                _accomodation=True
            else:
                _accomodation=False
            ListenRegisterUser = RegisteredUser(real_name = _name,user_gender=_gender,contact=_contact,accomodation=_accomodation)
            if not contrib_id == 0:
                ListenRegisterUser.user_register = cs
            querysetlist.append(ListenRegisterUser)   
            print(_accomodation)     
    RegisteredUser.objects.bulk_create(querysetlist)
    return contriblist(request,conf_id)
    
def subscribe(request,conf_id):
    if not request.session.get('user_id'):
        return login(request)
    user_id=request.session['user_id']
    if Bookmark.objects.filter(user_id=user_id,conference_id=conf_id):
        Bookmark.objects.filter(user_id=user_id, conference_id=conf_id).delete()
        return HttpResponse(0)
    else:
        Bookmark(user_id=user_id,conference_id=conf_id).save()
        return HttpResponse(1)

def if_subscribe(request, conf_id):
    if not request.session.get('user_id'):
        return login(request)
    user_id=request.session['user_id']
    if Bookmark.objects.filter(user_id=user_id,conference_id=conf_id):
        return HttpResponse(1)
    else:
        return HttpResponse(0)

#压缩文件
class InMemoryZip(object):
    def __init__(self):
        self.in_memory_zip = io.BytesIO()

    def append(self, filename_in_zip):
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)
        zf.write(filename_in_zip)

        for zfile in zf.filelist:
            zfile.create_system = 0       

        return self
    #添加压缩文件
    def appendfp(self, fp, path):
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)
        fp.seek(0)
        data = fp.read()
        zf.writestr(path,data)
        for zfile in zf.filelist:
            zfile.create_system = 0       

        return self

    def read(self):
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()
    #保存压缩文件
    def writetofile(self, filename):
        f = open(filename, "wb")
        f.write(self.read())
        f.close()

def ifexpire(request,conf_id):
    try:
        conf = Conference.objects.get(conf_id=conf_id)
    except:
        return error(request)
    if timezone.now() >= conf.submit_date_end:
        return HttpResponse(0)
    return HttpResponse(1)

def UPLOAD(file,pathname):
    with open(pathname, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
# 文件不存在时默认下载
def DOWNLOAD(path,filename):
    if not os.path.exists(path):
        path=settings.DEFAULT_DOWNLOAD_FILE
        filename='404.pdf'
    response = StreamingHttpResponse(readFile(path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=%s' % filename
    return response

def template_download(request,conf_id):
    try:
        conf=Conference.objects.get(conf_id=conf_id)
    except:
        return error(request)
    filename=conf.template
    path=os.path.join(settings.CONTRIBUTION_TEMPLATE_DIR,filename)
    return DOWNLOAD(path,filename)

def error(request):
    template = loader.get_template('error.html')
    return TemplateResponse(request,template)
