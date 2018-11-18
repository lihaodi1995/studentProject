from account.models import *
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission  

def add_permission(u, perm_str):
    content_type = ContentType.objects.get_for_model(User_Permission)
    permission = Permission.objects.get(content_type=content_type,
                                        codename=perm_str)
    u.user_permissions.add(permission)


def add_normal_user(email, password):
    u = User.objects.create_user(username=email, password=password, email=email)
    u.save()
    n = NormalUser.objects.create(
        user=u,
    )
    add_permission(u, 'NormalUser_Permission')
    u.save()

def add_org_user(email, password):
    u = User.objects.create_user(username=email, password=password, email=email)
    u.save()
    o = OrganizationUser.objects.create(
        user=u,
        org_name='BUAA',
        department='software',
        contacts='shiletong@buaa.edu.cn',
        phone_number='123123',
        address='xueyuanlu37',
    )
    add_permission(u, 'OrganizationUser_Permission')
    add_permission(u, 'ConferenceRelated_Permission')
    u.save()

#if __name__ == '__main__':
add_normal_user('714465499@qq.com', '123456')
add_org_user('shiletong@buaa.edu.cn', '123456')