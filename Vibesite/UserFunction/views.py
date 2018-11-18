from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect 
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.views import generic
from ConfManage.models import Conference
from UserAuth.views import *
from .models import Bookmark
def index(request):
    conferences = Conference.objects.all()
    template = loader.get_template('conference/conference_list.html')
    conferences = list(conferences)
    conferences.reverse()
    context = {
        'conferences': conferences,
    }
    return TemplateResponse(request, template, context)

def confDetail(request, conf_id):
    conf = Conference.objects.get(conf_id = conf_id)
    template = loader.get_template('conference/conference_detail.html')
    context = {
        'conf': conf,
    }
    return TemplateResponse(request, template, context)

def search(request):
    keyword = request.GET.get('keyword')
    error_msg = ''

    if not keyword:
        return
    conf = Conference.objects.filter(title__icontains = keyword)
    template = loader.get_template('conference/conference_list.html')
    context = {
        'conferences': conf,
    }
    return TemplateResponse(request, template, context)

def view_subscribed(request):
    if not request.session.get('user_id'):
        return login(request)
    user_id=request.session['user_id']

    conferences=Conference.objects.filter(bookmark__user_id=user_id)
    template = loader.get_template('conference/subscribed_list.html')
    context = {
        'conferences': conferences,
    }
    return TemplateResponse(request, template, context)

