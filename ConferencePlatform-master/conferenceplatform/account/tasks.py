from django.core.mail import send_mail
from celery import task

@task
def send_register_email(email):
    subject = '尊敬的' + email
    message = '您成功地在公平公正公开会议共享平台上注册了'
    to_email = list()
    to_email.append(email)
    send_mail(
        subject,
        message,
        'demonsNearby@163.com',
        to_email,
        fail_silently=False
    )


@task
def my_send_email(subject, message, to_email):
    send_mail(
        subject,
        message,
        'demonsNearby@163.com',
        to_email,
        fail_silently=False
    )
    