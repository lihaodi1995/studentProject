import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conferenceplatform.settings") 

import django
django.setup()
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from account.models import User_Permission
from django.db.transaction import atomic

from django.contrib.auth.models import User
if __name__ == '__main__':
    s_user = User.objects.filter(username = 'Admin')
    if len(s_user) != 0:
        print('already exist')
    else:
        with atomic():
            n_user = User.objects.create_user(
                username='Admin',
                password='321',
            )
            content_type = ContentType.objects.get_for_model(User_Permission)
            permission = Permission.objects.get(content_type=content_type,codename='AdminUser_Permission')
            n_user.save()
            n_user.user_permissions.add(permission)
            print('init_success')
            
        