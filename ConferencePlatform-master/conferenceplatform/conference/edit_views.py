from django.core.mail import send_mail
from conferenceplatform.settings import DEFAULT_FROM_EMAIL
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.db import transaction as database_transaction
from django.db import IntegrityError, DatabaseError
from django.utils import timezone
import datetime
import json
from account.models import *
from .models import *
from .forms import *
from .utils import *

from account.decorators import user_has_permission


def review_submission(request, id):
    assert request.method == 'POST'
    try:
        with database_transaction.atomic():
            sub = Submission.objects.get(pk=id)
            state = request.POST['state_choice']
            if state == 'P':
                sub.state = state
                con_name = sub.conference.title
                send_mail(subject='congratulations', message='your submission in ' + con_name + ' has been passed',
                          from_email=DEFAULT_FROM_EMAIL, ail_silently=False)
                return JsonResponse({'message': 'success'})
            elif state == 'R':
                sub.state = state
                # send email
                return JsonResponse({'message': 'success'})
            else:
                return JsonResponse({'message': 'invalid state choice'})
    except Submission.DoesNotExist:
        return JsonResponse({'message': 'invalid state choice'})


@user_has_permission('account.ConferenceRelated_Permission')
def edit_conference_by_id(request, id):
    class EditConForm(ConferenceInfoForm):
        paper_template = forms.FileField(required=False)
        activities = forms.CharField(required=False)

    assert request.method == 'POST'
    form = EditConForm(request.POST, request.FILES)
    if form.is_valid():
        with database_transaction.atomic():
            org = get_organization(request.user)
            assert org is not None
            try:
                conference = Conference.objects.get(pk=id)
                subject = Subject.objects.get(name=form.cleaned_data['subject'])
            except Subject.DoesNotExist:
                return JsonResponse({'message': 'unknown subject'})
            except Conference.DoesNotExist:
                return JsonResponse({'message': 'invalid conference id'})
            else:
                if conference.organization != org:
                    return JsonResponse({'message': 'invalid organization user'})

            conference.title = form.cleaned_data['title']
            conference.subject = subject
            conference.template_no = form.cleaned_data['template_no']
            conference.introduction = form.cleaned_data['introduction']
            conference.soliciting_requirement = form.cleaned_data['soliciting_requirement']
            conference.register_requirement = form.cleaned_data['register_requirement']
            conference.accept_due = form.cleaned_data['accept_due']
            conference.register_start = form.cleaned_data['register_start']
            conference.register_due = form.cleaned_data['register_due']
            conference.conference_start = form.cleaned_data['conference_start']
            conference.conference_due = form.cleaned_data['conference_due']
            conference.venue = form.cleaned_data['venue']

            if not valid_timepoints(conference):
                return JsonResponse({'message': 'timepoints not reasonable'})

            if 'activities' in request.POST:
                Activity.objects.filter(conference_id=conference.pk).delete()
                activities_json_str = form.cleaned_data['activities']
                activities_json = json.loads(activities_json_str)
                try:
                    for activity in activities_json:
                        add_activity(conference, activity)
                except KeyError:
                    return JsonResponse({'message': 'activity key error'})

            if 'paper_template' in request.FILES:
                conference.paper_template = request.FILES['paper_template']

            conference.save()
            return JsonResponse({'message': 'success'})

    else:
        return JsonResponse({'message': 'invalid uploaded data'})


@user_has_permission('account.ConferenceRelated_Permission')
def edit_activity_by_id(request, id):
    assert request.method == 'POST'
    form = ActivityInfoForm(request.POST)
    if form.is_valid():
        with database_transaction.atomic():
            org = get_organization(request.user)
            assert org is not None
            try:
                activity = Activity.objects.get(pk=id)
            except Activity.DoesNotExist:
                return JsonResponse({'message': 'invalid activity id'})
            else:
                if activity.conference.organization != org:
                    return JsonResponse({'message': 'invalid organization user'})

            activity.start_time = form.cleaned_data['start_time']
            activity.end_time = form.cleaned_data['end_time']
            activity.place = form.cleaned_data['place']
            activity.activity = form.cleaned_data['activity']
            activity.save()

            return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'invalid uploaded data'})
