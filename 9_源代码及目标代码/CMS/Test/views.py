from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader


def index(request):
    latest_question_list = 'Hello World,django'
    template = loader.get_template('base.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    #return HttpResponse(latest_question_list)
