from json import JSONDecodeError

from django.shortcuts import render
from django.http import JsonResponse
from .utils import *
from account.models import *
from account.decorators import user_has_permission
import json


def get_conference_detail(conference):
    data = {
        'organization': get_organization_detail(conference.organization),
        'title': conference.title,
        'subject': conference.subject.name,
        'introduction': conference.introduction,
        'soliciting_requirement': conference.soliciting_requirement,
        'paper_template': conference.paper_template.url,
        'register_requirement': conference.register_requirement,
        'accept_start': conference.accept_start,
        'accept_due': conference.accept_due,
        'modify_due': conference.modify_due,
        'register_start': conference.register_start,
        'register_due': conference.register_due,
        'conference_start': conference.conference_start,
        'conference_due': conference.conference_due,
        'template_no': conference.template_no,
        'venue': conference.venue,
    }
    return data


def get_organization_detail(org):
    data = {
        'org_id': org.pk,
        'org_name': org.org_name,
        'is_accepted': org.is_accepted,
        'department': org.department,
        'contacts': org.contacts,
        'phone_number': org.phone_number,
        'address': org.address,
        'email': org.user.username,
        'bussiness_license': org.bussiness_license.url,
        'id_card_front': org.id_card_front.url,
        'id_card_reverse': org.id_card_reverse.url,
    }
    return data


def get_activity_detail(activity):
    data = {
        'activity_id': activity.pk,
        'activity_name': activity.activity,
        'conference_id': activity.conference.pk,
        'conference_title': activity.conference.title,
        'start_time': activity.start_time,
        'end_time': activity.end_time,
        'place': activity.place,
    }
    return data


def get_submission_detail(submission):
    authors = json.loads(submission.authors)
    if str(submission.paper_old) == "":
        paper_old = None
    else:
        paper_old = submission.paper_old.url

    data = {
        'submitter_id': submission.submitter.pk,
        'conference_id': submission.conference.pk,
        'conference_title': submission.conference.title,
        'paper': submission.paper.url,
        'paper_name': submission.paper_name,
        'paper_old': paper_old,
        'paper_name_old': submission.paper_name_old,
        'paper_abstract': submission.paper_abstract,
        'authors': authors,
        'institute': submission.institute,
        'submit_time': submission.submit_time,
        'modification_advice': submission.modification_advice,
        'modified': submission.modified,
        'modified_time': submission.modified_time,
        'modified_explain': submission.modified_explain,
        'state': submission.state,
    }
    return data


def get_register_detail(info):
    par = json.loads(info.participants)
    data = {
        'user_id': info.user.pk,
        'conference_id': info.conference.pk,
        'submission_id': info.submission.pk,
        'participants': par,
        'pay_voucher': info.pay_voucher.url,
    }
    return data


def conference_information(request, id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        conference = Conference.objects.get(pk=id)
        data = get_conference_detail(conference)
        result['data'] = data
        result['message'] = 'success'
    except Conference.DoesNotExist:
        result['message'] = 'invalid conference pk'
    return JsonResponse(result)


def subject_information(request):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        subjects = Subject.objects.all()
        data = {'names': []}
        for i in subjects:
            data['names'].append(i.name)
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except Subject.DoesNotExist:
        result['message'] = ['no subjects']
        return JsonResponse(result)


def activity_information(request,id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        activity = Activity.objects.get(pk=id)
        data = get_activity_detail(activity)
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except Activity.DoesNotExist:
        result['message'] = ['invalid activity pk']
        return JsonResponse(result)


def submission_information(request,id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        submission = Submission.objects.get(pk=id)
        data = get_submission_detail(submission)
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except Submission.DoesNotExist:
        result['message'] = ['invalid submission pk']
        return JsonResponse(result)


def register_information(request, id):
    assert request.method == 'GET'
    result = {'message': ''}
    try:
        info = RegisterInformation.objects.get(pk=id)
        data = get_register_detail(info)
        result['data'] = data
        result['message'] = 'success'
        return JsonResponse(result)
    except RegisterInformation.DoesNotExist:
        result['message'] = ['invalid register information pk']
        return JsonResponse(result)


def top10_hot_conferences(request):
    ret = {'message':'success', 'data':[]}
    top10 = Conference.objects.order_by('-num_submission')[0:10]
    for c in top10:
        ret['data'].append({'pk': c.pk, 'title': c.title, 'subject': c.subject.name,
                            'organizationpk':c.organization.pk, 
                            'organization': c.organization.org_name, 
                            'conference_start': c.conference_start.strftime('%Y-%m-%d %H:%M:%S')})
    return JsonResponse(ret)

def count_conferences_based_on_subject(request):    
    try:
        name = request.GET['subject']
        subject = Subject.objects.get(name=name)
        n = subject.conference_set.count()
        return JsonResponse({'message': 'successs', 'data': n})
    except Subject.DoesNotExist:
        return JsonResponse({'message': 'invalid subject name'})

def count_conferences_for_all_subjects(request):
    ret = {'message': 'success', 'data': None}        
    data = dict()
    for s in Subject.objects.all():
        data[s.name] = s.conference_set.count()
    ret['data'] = data
    return JsonResponse(ret)    
