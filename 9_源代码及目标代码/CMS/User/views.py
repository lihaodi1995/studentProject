from django.shortcuts import render
from rest_framework import viewsets, response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from Paper.models import *
from Paper.serializers import *
from User.models import *
from User.serializers import *
from django.template import loader
from django.http import HttpResponse
import re, json
import collections
import hashlib


# Create your views here.

def checklen(pwd):
    return len(pwd) >= 6


def checkContainUpper(pwd):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False


def checkContainNum(pwd):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def checkContainLower(pwd):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(pwd)

    if match:
        return True
    else:
        return False


def checkSymbol(pwd):
    pattern = re.compile('([^a-z0-9A-Z])+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def checkPassword(pwd):
    # 判断密码长度是否合法
    lenOK = checklen(pwd)
    # 判断是否包含大写字母
    upperOK = checkContainUpper(pwd)
    # 判断是否包含小写字母
    lowerOK = checkContainLower(pwd)
    # 判断是否包含数字
    numOK = checkContainNum(pwd)
    # 判断是否包含符号
    symbolOK = checkSymbol(pwd)
    return (lenOK and upperOK and lowerOK and numOK and symbolOK)


def checkPhonenumber(phone):
    phone_pat = re.compile('1[3458]\\d{9}')
    return re.search(phone_pat, phone)


def checkUsername(username):
    username_pat = re.compile("[a-zA-z]\\w{0,9}")
    return re.search(username_pat, username)


def md5(arg):  # 这是加密函数，将传进来的函数加密
    arg = str(arg)
    return hashlib.md5(arg.encode(encoding='UTF-8')).hexdigest()


# return md5_pwd.hexdigest()#返回加密的数据

def info(msg):
    return json.dumps({'info': msg})


def errorInfo(msg):
    return json.dumps({'errorInfo': msg})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    @action(methods = ['GET'],detail = False)
    def index(self,request):
        return render(request,'judgement.html',status = status.HTTP_201_CREATED)

    @action(methods = ['POST'],detail = False)
    def login(self, request):
        if request.method == "POST":
            username = request.data.get('username')
            password = md5( request.data.get('password') )
            try:
                user = User.objects.get(username=username, password=password)
                if user:
                    request.session['is_login'] = 'true'         #定义session信息
                    request.session['username'] = username
                    request.session['id'] = user.id
                    request.session.set_expiry(0)
                    # template = loader.get_template('base.html')
                    # context = {}
                    return HttpResponse(info('success'), content_type="application/json")
            except:
                pass
                #return render(request,'base.html',status = status.HTTP_201_CREATED)                ## 登录成功就将url重定向到后台的url
        return HttpResponse(errorInfo('Username/Passwd is wrong'), content_type="application/json")

    @action(methods = ['GET'],detail = False)
    def logout(self, request):
        try:
            del request.session['is_login']         # 删除is_login对应的value值
            request.session.flush()                  # 删除django-session表中的对应一行记录
        except KeyError:
            pass
        template = loader.get_template('login.html')
        context = {}
        return HttpResponse(template.render(context, request))
        #return render(request,'base.html')             #重定向回主页面


    @action(methods = ['POST'],detail = False)
    def register(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        password2 = request.data.get("password2")
        email = request.data.get("email")
        tel = request.data.get("tel")
        if not checkUsername(username):    #必须以字母开头，长度在10位以内
           return  HttpResponse(errorInfo("用户名不合法"), content_type="application/json")
        if not checkPassword(password):    #包含大写、小写、符号；长度大于等于8
           return  HttpResponse(errorInfo("密码不合法"), content_type="application/json")
        if not password == password2:
           return  HttpResponse(errorInfo("两次密码不一致"), content_type="application/json")
        if not checkPhonenumber(tel):      #手机号位数为11位；开头为1，第二位为3或4或5或8;
           return  HttpResponse(errorInfo("电话号码不合法"), content_type="application/json")   
        user_serializer = UserSerializer(data = request.data)
        password = md5(password)
        if user_serializer.is_valid():
            thisUser = User(
                username = username,
                password = password,
                email = email,
                tel = tel,
                ).save()   
            return HttpResponse(info("success"), content_type="application/json")
            #return render(request,'login.html',status = status.HTTP_201_CREATED)
        return HttpResponse(errorInfo("未知原因失败，请稍后再试"), content_type="application/json") 

    @action(methods = ['GET'],detail = False)
    def info(self, request):
        try:
            pk = request.GET.get("username")
            thisuser = User.objects.get(username = pk)
            result = list()
            result.append(UserSerializer(thisuser).data)
            papers = thisuser.Paper_set.all()
            for paper in papers:
                result.append(PaperSerializer(paper).data)
        except:
            a = collections.OrderedDict({"errorInfo":"服务器出错，请稍后重试。"})
            return Response(a, status = status.HTTP_400_BAD_REQUEST)
        return Response(result, status = status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def registermeeting(self, request):
        meeting_id = request.data.get("meeting_id")
        user_id = request.data.get("user_id")
        paper_id = request.data.get("paper_id")
        people_name=request.data.get("people_name")
        people_sex=request.data.get("people_sex")
        isbook=request.data.get("isbook")
        #缴费凭证pdf或者照片
        thispaper = Paper.objects.get(id=paper_id)
        print(111)
        if thispaper.status == 1:
            thisuser = User.objects.get(id=user_id)
            thismeeting = Meeting.objects.get(meeting_id=meeting_id)
            thisuser.participate.add(thismeeting)
            return Response({"info": "register meeting success"}, status=status.HTTP_200_OK)
        return Response({"errorInfo": "paper is not received"}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def contribute(self, request):
        user_id = request.data.get("user_id")
        thisuser = User.objects.get(id=user_id)
        meeting_id=request.data.get("meeting_id")
        thismeeting=Meeting.objects.get(meeting_id=meeting_id)
        thispaper= Paper(author_1=request.data.get("author_1"),
            author_2=request.data.get("author_2"),
            author_3=request.data.get("author_3"),
            title=request.data.get("title"),
            abstract=request.data.get("abstract"),
            keyword=request.data.get("keyword"),
            content=request.FILES['content'],
            #content=request.data.get("content"),
            status=-1,
            owner=thisuser,
            meeting=thismeeting,
        )
        thispaper.save()
        thisuser.participate.add(thismeeting)
        return Response("info: contribute succsss", status=status.HTTP_200_OK)


    @action(methods=['POST'], detail=False)
    def favorite(self, request):
        user_id = request.data.get("user_id")
        thisuser = User.objects.get(id=user_id)
        meeting_id = request.data.get("meeting_id")
        thismeeting = Meeting.objects.get(meeting_id=meeting_id)
        thisuser.favorite.add(thismeeting)
        return Response({"info":"favorite succsss"}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail = False)
    def allpaper(self,request):
        pk = request.query_params.get('pk', None)
        thisuser = User.objects.get(id=pk)
        papers = thisuser.paper_set.all()
        template = loader.get_template('judgement.html')
        context = {
            'papers': papers,
        }
        return HttpResponse(template.render(context, request))

