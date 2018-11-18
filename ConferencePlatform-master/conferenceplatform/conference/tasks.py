from account.tasks import my_send_email
from django.core.mail import send_mass_mail
from celery import task
from conference.models import *
from account.models import *
from datetime import datetime, timedelta
from .email import *


@task
def send_register_start_email():
    today = datetime.now()
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter(register_start__range=(today, day))
    messages = []
    for conference in conferences:
        collect_users = conference.collect_user.all()
        for user in collect_users:
            messages.append((SUBJECT['register_start'],
                             MESSAGE['register_start'].format(user.user.username, conference.title, conference.register_due),
                             FROM_EMAIL,
                             [user.user.username]))
    send_mass_mail(messages, fail_silently=False)
    return True


@task
def send_register_due_email():
    today = datetime.now()
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter(register_due__range=(today, day))
    messages = []
    for conference in conferences:
        collect_users = conference.collect_user.all()
        for user in collect_users:
            messages.append((SUBJECT['register_due'],
                             MESSAGE['register_due'].format(user.user.username, conference.title, conference.register_due),
                             FROM_EMAIL,
                             [user.user.username]))
    send_mass_mail(messages, fail_silently=False)
    return True


@task
def send_accept_due_email():
    today = datetime.now()
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter(accept_due__range=(today, day))
    messages = []
    for conference in conferences:
        collect_users = conference.collect_user.all()
        for user in collect_users:
            messages.append((SUBJECT['accept_due'],
                             MESSAGE['accept_due'].format(user.user.username, conference.title, conference.accept_due),
                             FROM_EMAIL,
                             [user.user.username]))
    send_mass_mail(messages, fail_silently=False)
    return True


@task
def send_modify_due_email():
    today = datetime.now()
    day = datetime.now() + timedelta(days=1)
    conferences = Conference.objects.filter(modify_due__range=(today, day))
    messages = []
    for conference in conferences:
        submissions = conference.submission_set.filter(state='M')
        for submission in submissions:
            messages.append((SUBJECT['modify_due'],
                             MESSAGE['modify_due'].format(submission.submitter.user.username, conference.title, conference.modify_due),
                             FROM_EMAIL,
                             [submission.submitter.user.username]))
    send_mass_mail(messages, fail_silently=False)
    return True
