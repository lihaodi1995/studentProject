from django import forms
from django.db import models
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User
from django.views import generic
from .forms import RegisterForm, EditForm
from django.template.response import TemplateResponse
# Create your views here.
class UserForm(forms.Form):
    user_name = forms.CharField(label='用户名', max_length=32, widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='密码', max_length=32,widget=forms.PasswordInput(attrs={'class':'form-control'}))

def register(request):
    if request.session.get('is_login',None):
        # 登录状态不允许注册，规则可以修改
        return redirect('/index/')
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid(): # 获取数据
            user_name = register_form.cleaned_data['user_name']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2: #判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'UserAuth/register.html', locals())
            else:
                same_name_user =User.objects.filter(user_name=user_name)
                if same_name_user: # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'UserAuth/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user: # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'UserAuth/register.html', locals())
                # 创建新用户
                new_user = User.objects.create()
                new_user.user_name = user_name
                new_user.password = password1
                new_user.email = email
                new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request,'UserAuth/register.html',locals())

def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == "POST":
        login_form =UserForm(request.POST)
        message = "所有字段都必须填写！"
        
        print(login_form.is_valid())
        
        if login_form.is_valid():
            user_name = login_form.cleaned_data['user_name']
            password = login_form.cleaned_data['password']
            # 用户名字符合性验证
            # 密码长度验证
            # 更多的其他验证...
            try:
                user = User.objects.get(user_name=user_name)
                if user.password == password:
                    print ("login success!")
                    # session 保存，需要任何数据都可以往里面写
                    request.session['is_login'] = True
                    request.session['user_id'] = user.user_id
                    request.session['user_name'] = user.user_name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'UserAuth/login.html',locals())
    login_form =UserForm()
    return render(request,'UserAuth/login.html',locals())

def index(request):
    pass
    return render(request,'UserAuth/index.html')

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一回事
        return redirect('/index/')
    request.session.flush()
    return redirect('/index')

def userinfo(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    user_name = user.user_name
    email = user.email
    group = user.group
    group_name = None
    if group is not None:
        group_name = user.group.group_name
    # print(str(user_id)+user_name+email+'..'+group_name)
    context = {
        'user_id':user_id,
        'user_name': user_name,
        'email': email,
        'group_name': group_name
    }
    return TemplateResponse(request,'UserAuth/userinfo.html',context)

def infoedit(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    if request.method == 'POST':
        edit_form = EditForm(request.POST)
        user_id = request.session.get('user_id')
        user = User.objects.get(user_id = user_id)
        message = "请检查填写的内容！"
        if edit_form.is_valid():
            print('表单生成')
            #new_user_name = edit_form.cleaned_data['user_name']
            new_password1 = edit_form.cleaned_data['password1']
            new_password2 = edit_form.cleaned_data['password2']
            new_email = edit_form.cleaned_data['email']
            if new_password1 != new_password2:
                message = "两次输入的密码不同！"
                return TemplateResponse(request,'UserAuth/infoedit.html', locals())
            else:
                # is_same_name_user = User.objects.filter(user_name = new_user_name)
                # if is_same_name_user:
                #     message = '用户已经存在，请重新选择用户名'
                #     return render(request,'UserAuth/infoedit.html', locals())
                is_same_email_user = User.objects.filter(email = new_email)
                if is_same_email_user:
                    message = '该邮箱地址已被占用，请使用其他邮箱！'
                    return TemplateResponse(request,'UserAuth/infoedit.html', locals())
                # user.user_name = new_user_name
                user.password = new_password1
                user.email = new_email
                user.save()
                print('成功修改')
                message = '修改成功！'
                group = user.group
                group_name = None
                if group is not None:
                    group_name = user.group.group_name
                context = {
                    'user_id':user_id,
                    'user_name':user.user_name,
                    'email':user.email,
                    'group_name':group_name,
                }
                return TemplateResponse(request,'UserAuth/userinfo.html', context)
    edit_form =EditForm()
    return TemplateResponse(request,'UserAuth/infoedit.html', locals())