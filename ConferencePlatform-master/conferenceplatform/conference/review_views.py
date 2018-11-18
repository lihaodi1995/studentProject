from django.http import JsonResponse
from .utils import *
from account.decorators import user_has_permission
from django.db import transaction as database_transaction
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from django import forms
from account.tasks import my_send_email
from django.core.mail import send_mail
from .email import *


@user_has_permission('account.ConferenceRelated_Permission')
def review_submission(request, id):
    assert request.method == 'POST'
    cleaner = forms.CharField()
    try:
        with database_transaction.atomic():
            sub = Submission.objects.get(pk=id)
            conf = sub.conference
            org_login = get_organization(request.user)
            if org_login == None or org_login.pk != conf.organization.pk:
                return JsonResponse({'message': 'permission error'})
            conf_status = conference_status(conf)

            state = cleaner.clean(request.POST['state_choice'])
            sub.state = state
            con_name = sub.conference.title
            sub_info = dict(username=sub.submitter.user.username,
                            conference=con_name,
                            paper=sub.paper_name,
                            submission=sub.pk)
            if state == 'P':
                if not sub.modified:
                    subject = SUBJECT['first_passed']
                    message = MESSAGE['first_passed'].format(sub_info)
                else:
                    subject = SUBJECT['modification_passed']
                    message = MESSAGE['modification_passed'].format(sub_info)
            elif state == 'R':
                advice = cleaner.clean(request.POST['advice'])
                sub.modification_advice = advice
                sub_info['advice'] = advice
                if not sub.modified:
                    subject = SUBJECT['first_rejected']
                    message = MESSAGE['first_rejected'].format(sub_info)
                else:
                    subject = SUBJECT['modification_rejected']
                    message = MESSAGE['modification_rejected'].format(sub_info)
            elif state == 'M':
                if conf_status != ConferenceStatus.reviewing_accepting_modification:
                    return JsonResponse({'message': 'not in modification period'})
                advice = cleaner.clean(request.POST['advice'])
                sub.modification_advice = advice
                sub_info['advice'] = advice
                sub_info['modify_due'] = conf.modify_due
                subject = SUBJECT['need_modified']
                message = MESSAGE['need_modified'].format(sub_info)
            else:
                return JsonResponse({'message': 'invalid state choice'})
            sub.save()
            my_send_email.delay(subject, message, [sub.submitter.user.username])
            # send_mail(subject, message, FROM_EMAIL, [sub.submitter.user.username], fail_silently=False)
            return JsonResponse({'message': 'success'})
    except Submission.DoesNotExist:
        return JsonResponse({'message': 'invalid submission pk'})
    except MultiValueDictKeyError:
        return JsonResponse({'message': 'invalid uploaded data'})
    except ValidationError:
        return JsonResponse({'message': 'invalid uploaded data'})
