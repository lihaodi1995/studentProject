from django.shortcuts import render
from django.http import JsonResponse
from account.decorators import user_has_permission
from conference.models import *
from .models import *
from conference.utils import get_organization
from conference import detail_views
from account import decorators
from .tasks import my_send_email
from django.core.mail import send_mail
from conference.email import *


def test1(request):
    to_email = ['chd19970620@163.com']
    con = Conference.objects.filter()
    for conference in con:
        submissions = conference.submission_set.filter(state='M')
        for submission in submissions:
            send_mail(SUBJECT['modify_due'],
                      MESSAGE['modify_due'].format(submission.submitter.user.username, conference.title, conference.modify_due),
                      'demonsNearby@163.com',
                      to_email, fail_silently=False)
    return JsonResponse({'123': '123'})


@user_has_permission('account.ConferenceRelated_Permission')
def get_conferences_by_organization(request):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        org = get_organization(request.user)
        if org is None:
            return JsonResponse({'message': 'permission error'})
        #conferences = Conference.objects.filter(organization=org)
        conferences = org.conference_set.all()
        data = []
        for con in conferences:
            data.append({
                'conference_id': con.pk,
                'conference_title': con.title,
            })
        result['data'] = data
        result['message'] = 'success'
    except Conference.DoesNotExist:
        result['message'] = ['no conference']
    except OrganizationUser.DoesNotExist:
        result['message'] = ['invalid organization user']
    except OrganizationSubUser.DoesNotExist:
        result['message'] = ['invalid organization sub user']
    return JsonResponse(result)


@user_has_permission('account.NormalUser_Permission')
def get_submissions_by_submitter(request, state=None):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        submitter = request.user.normaluser
        if state is None:
            submissions = submitter.submission_set.all()
        else:
            submissions = Submission.objects.filter(submitter=submitter, state=state)
        data = []
        for sub in submissions:
            data.append({
                'submission_id': sub.pk,
                'paper_name': sub.paper_name,
                'conference_title': sub.conference.title,
                'state': sub.state,
            })
        result['data'] = data
        result['message'] = 'success'
    except AttributeError:
        result['message'] = ['invalid request user']
    return JsonResponse(result)


@user_has_permission('account.ConferenceRelated_Permission')
def get_papers_by_conference(request, id):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        conference = Conference.objects.get(pk=id)
        if conference.organization.user != request.user:
            return JsonResponse({'message': 'permission error'})
        #papers = Submission.objects.filter(conference=conference)
        papers = conference.submission_set.all()
        data = []

        for paper in papers:
            try:
                paper_url = paper.paper.url
            except ValueError:
                paper_url = None
            if str(paper.paper_old) == "":
                paper_old = None
            else:
                paper_old = paper.paper_old.url
            data.append({
                'submission_id': paper.pk,
                'paper_name': paper.paper_name,
                'paper_url': paper_url,
                'state': paper.state,
                'submitter': paper.submitter.user.username,
                'modification_advice': paper.modification_advice,
                'modified': paper.modified,
                'paper_old': paper_old,
                'paper_name_old': paper.paper_name_old,
            })
        result['data'] = data
        result['message'] = 'success'
    except Submission.DoesNotExist:
        result['message'] = ['no submissions']
    except Conference.DoesNotExist:
        result['message'] = ['no conference']
    return JsonResponse(result)


def get_activities_by_conference(request, id):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        conference = Conference.objects.get(pk=id)
        #activities = Activity.objects.filter(conference=conference)
        activities = conference.activity_set.all()
        data = []
        for activity in activities:
            data.append({
                'activity_id': activity.pk,
                'activity_name': activity.activity,
                'start_time': activity.start_time,
                'end_time': activity.end_time,
                'place': activity.place,
            })
        result['data'] = data
        result['message'] = 'success'
    except Activity.DoesNotExist:
        result['message'] = ['no activities']
    except Conference.DoesNotExist:
        result['message'] = ['no conference']
    return JsonResponse(result)


@user_has_permission('account.OrganizationUser_Permission')
def get_subuser_by_org(request):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        #org = OrganizationUser.objects.get(user=request.user)
        #subusers = OrganizationSubUser.objects.filter(organization=org)
        subusers = request.user.organizationuser.organizationsubuser_set.all()
        data = []
        for sub in subusers:
            data.append({
                'sub_user_id': sub.pk,
                'sub_username': sub.user.username,
                'sub_password': sub.user.password,
            })
        result['data'] = data
        result['message'] = 'success'
    except AttributeError:
        result['message'] = ['invalid organization user']
    return JsonResponse(result)


def get_images_by_org(request, id):
    assert request.method == 'GET'
    result = {'message': '', 'data': {}}
    try:
        org = OrganizationUser.objects.get(pk=id)
        data = detail_views.get_organization_detail(org)
        result['data'] = data
        result['message'] = 'success'
    except OrganizationUser.DoesNotExist:
        result['message'] = ['invalid organization user']
    return JsonResponse(result)


@user_has_permission('account.ConferenceRelated_Permission')
def get_detail_by_request_org(request):
    assert request.method == 'GET'
    result = {'message': '', 'data': {}}
    try:
        org = get_organization(request.user)
        data = detail_views.get_organization_detail(org)
        result['data'] = data
        result['message'] = 'success'
    except AttributeError:
        result['message'] = ['invalid organization user']
    return JsonResponse(result)


@user_has_permission('account.ConferenceRelated_Permission')
def get_registrations_by_conference(request, id):
    assert request.method == 'GET'
    result = {'message': '', 'data': []}
    try:
        conference = Conference.objects.get(pk=id)
        if conference.organization.user != request.user:
            return JsonResponse({'message': 'permission error'})
        registrations = conference.registerinformation_set.all()
        data = []
        for registration in registrations:
            paper_info = {}
            if registration.submission is not None:
                paper_info.update({
                    'paper_id': registration.submission.pk,
                    'paper_name': registration.submission.paper_name,
                })
            try:
                voucher_url = registration.pay_voucher.url
            except ValueError:
                voucher_url = None
            data.append({
                'registration_id': registration.pk,
                'paper_info': paper_info,
                'participants': registration.participants,
                'pay_voucher': voucher_url,
            })
        result['data'] = data
        result['message'] = 'success'
    except Conference.DoesNotExist:
        result['message'] = ['invalid conference id']
    return JsonResponse(result)