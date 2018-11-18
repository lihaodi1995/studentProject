from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from Institution.models import Institution,Employee
from Institution.serializers import InstitutionSerializer,EmployeeSerializer
from django.template import loader
from django.http import HttpResponse
import re,json
import hashlib
# Create your views here.
def checklen(pwd):
	return len(pwd)>=8

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
	#判断密码长度是否合法
	lenOK=checklen(pwd)
	#判断是否包含大写字母
	upperOK=checkContainUpper(pwd)
	#判断是否包含小写字母
	lowerOK=checkContainLower(pwd)
	#判断是否包含数字
	numOK=checkContainNum(pwd)
	#判断是否包含符号
	symbolOK=checkSymbol(pwd)
	return (lenOK and upperOK and lowerOK and numOK and symbolOK)

def checkPhonenumber(phone):
	phone_pat = re.compile('1[3458]\\d{9}')
	return re.search(phone_pat, phone)

def checkUsername(username):
	username_pat = re.compile("[a-zA-z]\\w{0,9}")
	return re.search(username_pat, username)

def info(msg):
	return json.dumps({'info': msg})

def errorInfo(msg):
	return json.dumps({'errorInfo': msg})

def md5(arg):#这是加密函数，将传进来的函数加密
	arg = str(arg)
	return hashlib.md5(arg.encode(encoding='UTF-8')).hexdigest()

class InstitutionViewSet(viewsets.ModelViewSet):
	queryset = Institution.objects.all()
	serializer_class = InstitutionSerializer

	@action(methods = ['POST'],detail = False)
	def register(self, request):
	    name = request.data.get("name")
	    corporate_id = request.data.get("corporate_id")
	    place = request.data.get("place")
	    legal_person = request.data.get("legal_person")
	    establish_date = request.data.get("establish_date")
	    type = request.data.get("type")
	    username = request.data.get("username")
	    password = request.data.get("password")
	    password2 = request.data.get("password2")
	    email = request.data.get("email")
	    tel = request.data.get("tel")
	    try:
	        if Institution.objects.get( name = name):
	            return  HttpResponse(errorInfo("该机构已存在"), content_type="application/json")
	        if Employee.objects.get(username = username):
	            return  HttpResponse(errorInfo("用户名已存在"), content_type="application/json")
	    except:
	    	pass
	    if not checkUsername(name):    #必须以字母开头，长度在10位以内
	        return  HttpResponse(errorInfo("机构名不合法"), content_type="application/json")
	    if not checkUsername(username):    #必须以字母开头，长度在10位以内
	        return  HttpResponse(errorInfo("用户名不合法"), content_type="application/json")
	    if not checkPassword(password):    #包含大写、小写、符号；长度大于等于8
	        return  HttpResponse(errorInfo("密码不合法"), content_type="application/json")
	    if not password == password2:
	        return  HttpResponse(errorInfo("两次密码不合法"), content_type="application/json")
	    if  not checkPhonenumber(tel):      #手机号位数为11位；开头为1，第二位为3或4或5或8;
	        return  HttpResponse(errorInfo("电话号码不合法"), content_type="application/json")   
	    institution_serializer = InstitutionSerializer(data = request.data)
	    employee_serializer = EmployeeSerializer(data = request.data)
	    password = md5(password)
	    if institution_serializer.is_valid():
	        if employee_serializer.is_valid():
	            thisInstitution = Institution(
	                name = name,
	                corporate_id = corporate_id,
	                place = place,
	                legal_person = legal_person,
	                establish_date = establish_date,
	                status="0",
	                type = type,
	                )
	            thisInstitution.save()
	            thisEmployee = Employee(
	                username = username,
	                password = password,
	                email = email,
	                tel = tel,
	                institution = thisInstitution,
	                )
	            thisEmployee.save()
	            return HttpResponse(info("success"), content_type="application/json")
	        #return render(request,'login.html',status = status.HTTP_201_CREATED)
	        
	    return HttpResponse(errorInfo("未知原因失败，请稍后再试"), content_type="application/json") 

class EmployeeViewSet(viewsets.ModelViewSet):
	queryset = Employee.objects.all()
	serializer_class = EmployeeSerializer

	@action(methods = ['POST'],detail = False)
	def login(self, request):
	    if request.method == "POST":
	        username = request.data.get('username')
	        password = request.data.get('password')
	        password = md5(password)
	        try:
	            employee = Employee.objects.get(username=username, password=password)
	            if employee:
	                request.session['is_login'] = 'true'         #定义session信息
	                request.session['username'] = username
	                request.session['id'] = employee.id
	                request.session.set_expiry(0)
	            return HttpResponse(info("success"), content_type="application/json")
	        except:
	            pass
	            #return render(request,'base.html',status = status.HTTP_201_CREATED)                ## 登录成功就将url重定向到后台的url
	    return HttpResponse(errorInfo('用户名或密码错误'), content_type="application/json")

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
	def registerother(self, request):
	    if not request.session['is_login']:
	       return  HttpResponse(errorInfo("请登入后操作"), content_type="application/json") 
	    username = request.data.get("username")
	    password = request.data.get("password")
	    password2 = request.data.get("password2")
	    email = request.data.get("email")
	    tel = request.data.get("tel")
	    try:
	       if not Employee.objects.get(username = username):
	           return  HttpResponse(errorInfo("用户名已存在"), content_type="application/json")
	    except:
	        pass
	    if not checkUsername(username):    #必须以字母开头，长度在10位以内
	       return  HttpResponse(errorInfo("用户名不合法"), content_type="application/json")
	    if not checkPassword(password):    #包含大写、小写、符号；长度大于等于8
	       return  HttpResponse(errorInfo("密码不合法"), content_type="application/json")
	    if not password == password2:
	       return  HttpResponse(errorInfo("确认密码不一致"), content_type="application/json")
	    if not checkPhonenumber(tel):      #手机号位数为11位；开头为1，第二位为3或4或5或8;
	       return  HttpResponse(errorInfo("电话号码不合法"), content_type="application/json")   
	    employee_serializer = EmployeeSerializer(data = request.data)
	    password = md5(password)
	    try:
	        thisEmployee = Employee.objects.get(username=request.session['username'])
	    except:
	        pass
	    if employee_serializer.is_valid():
	        otherEmployee = Employee(
	            username = username,
	            password = password,
	            email = email,
	            tel = tel,
	            institution = thisInstitution.institution,
	            )
	        otherEmployee.save()
	        template = loader.get_template('login.html')
	        context = {}
	        return HttpResponse(template.render(context, request))
	        #return render(request,'login.html',status = status.HTTP_201_CREATED)
	    return  HttpResponse(errorInfo("未知原因失败，请稍后再试"), content_type="application/json") 