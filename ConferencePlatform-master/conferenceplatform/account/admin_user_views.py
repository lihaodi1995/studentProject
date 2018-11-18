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
from .tasks import my_send_email


@user_has_permission('account.AdminUser_Permission')
def process_orgnization_register(request):
    assert request.method == 'POST'
    data = {'message' :''}
    form = ProcessorgregForm(request.POST)
    if form.is_valid() is False:
        data['message'] = 'format error'
        return JsonResponse(data)
    org_pk = form.cleaned_data['org_pk']
    is_accepted = form.cleaned_data['is_accepted']
    
    org = OrganizationUser.objects.filter(pk = org_pk)
    if len(org) == 0:
        data['message'] = 'organization not exist'
        return JsonResponse(data)
    org = org[0]

    with atomic():
        data['message'] = 'success'
        if is_accepted == 'pass':
            org.is_accepted = 'P'
            org.save()
            org_user = org.user
            org_user.is_active = True
            org_user.save()
            my_send_email.delay(
                subject='尊敬的'+org_user.username,
                message='恭喜，你通过了审核',
                to_email=[org_user.username,]
            )
        elif is_accepted == 'reject':
            org.is_accepted = 'R'
            org.save()
            org_user  = org.user
            my_send_email.delay(
                subject='尊敬的'+org_user.username,
                message='抱歉，审核不通过',
                to_email=[org_user.username,]
            )
        else:
            data['message'] = 'format error'
    return JsonResponse(data)

@user_has_permission('account.AdminUser_Permission')
def process_org_list(request):
    data = {'message' :'', 'data':[]}
    org_list = OrganizationUser.objects.filter(is_accepted = 'M')
    data['message'] = 'success'
    for org in org_list:
        data['data'].append({'id':org.pk, 'name': org.org_name})
    return JsonResponse(data)
    
