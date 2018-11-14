# coding=utf8
import datetime
import math

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.models import *


def login(request):
    user = None
    if request.POST:
        result = False
        try:
            user = User.objects.get(id=request.POST['id'])
            if user.password == request.POST['password']:
                result = True
        except Exception as e:
            result = False
            print(e)
        if result:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            try:
                time = datetime.date.today()
                semester = Semester.objects.get(start_time__lte=time, end_time__gte=time)
                current_week = math.ceil((time - semester.start_time).days / 7)
                request.session['current_week'] = current_week
            except Exception as e:
                print(e)
            if user.role == 1:
                return HttpResponseRedirect(reverse('admin:index'))
            elif user.role == 2:
                return HttpResponseRedirect(reverse('teachers:index'))
            else:
                return HttpResponseRedirect(reverse('students:index'))
        else:
            return HttpResponse("<script>alert('用户名或密码错误!');window.location.href='/login/';</script>")

    else:
        return render(request, 'users/login.html')


def logout(request):
    if request.session.get('user_id', None):
        del request.session['user_id']
    if request.session.get('user_name', None):
        del request.session['user_name']
    return HttpResponseRedirect(reverse('login'))


def changePassword(request):
    result = False
    try:
        if request.POST:
            user = User.objects.get(id=request.session['id'], password=request.POST['oldPassword'])
            user.password = request.POST['newPassword']
            user.save()
            result = True

    except Exception as e:
        print(e)

    if request.POST:
        if result:
            return HttpResponse("修改成功")
        else:
            return HttpResponse("修改失败")
    else:
        return render(request, 'admin/setPassword.html')
