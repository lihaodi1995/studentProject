from django.contrib import admin

# Register your models here.
from .models import Group
from .models import Authorization

admin.site.register(Group)
admin.site.register(Authorization)