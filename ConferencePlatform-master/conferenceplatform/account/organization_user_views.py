from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import *
from django.contrib.auth.models import User
from django.db.transaction import atomic, DatabaseError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from .forms import OrganizationUserRegisterForm
from .tasks import my_send_email

#我们在这里用email来作为username
def organization_user_register(request):
    
    assert request.method == 'POST'
    data = {'message':'', 'data':{}}

    form = OrganizationUserRegisterForm(request.POST, request.FILES)
    if form.is_valid() is False:
        data['message'] = 'format error'
        return JsonResponse(data, safe=False)
    
    username = form.cleaned_data['username']
    password =form.cleaned_data['password']
    confirm_password =form.cleaned_data['confirm_password']
    org_name =form.cleaned_data['org_name']
    department =form.cleaned_data['department']
    contacts =form.cleaned_data['contacts']
    phone_number =form.cleaned_data['phone_number']
    address =form.cleaned_data['address']
    bussiness_license = form.cleaned_data['bussiness_license']
    id_card_front = form.cleaned_data['id_card_front']
    id_card_reverse = form.cleaned_data['id_card_reverse']
    
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
            permission = Permission.objects.get(content_type=content_type,codename='OrganizationUser_Permission')
            permission2 = Permission.objects.get(content_type=content_type, codename='ConferenceRelated_Permission')
            new_user.is_active = False
            new_user.save()
            new_user.user_permissions.add(permission, permission2)
            organization_user = OrganizationUser(
                user = new_user,
                org_name = org_name,
                department= department,
                contacts = contacts,
                phone_number = phone_number,
                address = address,
                bussiness_license = bussiness_license,
                id_card_front = id_card_front,
                id_card_reverse = id_card_reverse,
            )

            organization_user.save()
            data['message'] = 'success'
            my_send_email.delay(
                subject='尊敬的'+username,
                message='请您静静等待管理员的审核',
                to_email=[username,]
            )
    except DatabaseError as e:
        data['message'] = str(e)
    
    return JsonResponse(data, safe=False)
