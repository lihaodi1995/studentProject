from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.

class UserRender(object):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    @property
    def namefirst(self):
        return self.name[0]

def index(request):
    return TemplateResponse(request, 'base.html', {
        #'user': UserRender('Yang')
    })
