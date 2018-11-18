from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.db.transaction import atomic, DatabaseError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .forms import *
from .decorators import user_has_permission
from conference.models import Conference
from .tasks import send_register_email


#我们在这里用email来作为username
def normal_user_register(request):
    assert request.method == 'POST'
    data = {'message':'', 'data':{}}
    form = NormalUserRegisterForm(request.POST)
    if form.is_valid() is False:
        data['message'] = 'format error'
        return JsonResponse(data, safe=False)
    
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    confirm_password = form.cleaned_data['confirm_password']


    if password != confirm_password:
        data['message'] = 'password error'
        return JsonResponse(data, safe=False)
    search_user = User.objects.filter(username__icontains = username)
    if len(search_user) != 0:
        data['message'] = 'username error'
        return JsonResponse(data, safe=False)
    
    try:
        with atomic():
            new_user = User.objects.create_user(username, email=username, password=password)
            
            content_type = ContentType.objects.get_for_model(User_Permission)
            permission = Permission.objects.get(content_type=content_type,codename='NormalUser_Permission')
            new_user.save()
            new_user.user_permissions.add(permission)
            normal_user = NormalUser(user=new_user)
            normal_user.save()
            data['message'] = 'success'
            send_register_email.delay(username)
    except DatabaseError:
        data['message'] = 'database error'
    return JsonResponse(data, safe=False)

@user_has_permission('account.NormalUser_Permission')
def collect(request, pk):
    data = {'message':'', 'data':{}}
    assert request.method == 'POST'
    conf = Conference.objects.filter(pk = pk)
    if len(conf) == 0:
        data['message'] = "conference not exist"
        return JsonResponse(data)
    conf = conf[0]
    conf.collect_user.add(request.user.normaluser)
    data['message'] = 'susccess'
    return JsonResponse(data)

@user_has_permission('account.NormalUser_Permission')
def discollect(request, pk):
    data = {'message':'', 'data':{}}
    assert request.method == 'POST'
    conf = Conference.objects.filter(pk = pk)
    if len(conf) == 0:
        data['message'] = "conference not exist"
        return JsonResponse(data)
    conf = conf[0]
    conf.collect_user.remove(request.user.normaluser)
    data['message'] = 'susccess'
    return JsonResponse(data)

@user_has_permission('account.NormalUser_Permission')
def collect_list(request):
    data = {'message':'', 'data':[]}
    conf_list = request.user.normaluser.collections.all()
    
    data['message'] = 'success'
    for conf in conf_list:
        data['data'].append({'id':conf.pk, 'title': conf.title})
    
    return JsonResponse(data)

@user_has_permission('account.NormalUser_Permission')
def is_collected(request, pk):
    data = {'message':'', 'data':{}}
    conf = Conference.objects.filter(pk = pk)
    if len(conf) == 0:
        data['message'] = "conference not exist"
        return JsonResponse(data)
    conf = conf[0]
    user = conf.collect_user.all().filter(user = request.user.normaluser)
    if len(user) == 0:
        data['data']['collected'] = False
    else:
        data['data']['collected'] = True
    data['message'] = 'susccess'
    return JsonResponse(data)
