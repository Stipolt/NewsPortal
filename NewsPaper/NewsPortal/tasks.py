from datetime import datetime, timedelta
from NewsPaper.celery import app

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, User


@shared_task
def hello():
    time.sleep(1)
    print("Hello, world!")


# отправка новых новостей
@shared_task()
def send_to_sub(post, email_subs):
    html_content = render_to_string(
        'send_mail_post.html',
        {'post': post}
    )
    msg = EmailMultiAlternatives(
        subject=f'{post.header} ',
        body=f'{post.content}',
        from_email='egorkabox@yandex.ru',
        to=email_subs,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# рассылка каждый понедельник(вызов в celery)
@shared_task()
def send_last_news():
    end_date = datetime.now()  # replace(hour=8, minute=0, second=0)
    start_date = end_date - timedelta(weeks=1)
    qs_post = Post.objects.filter(time_post__range=(start_date, end_date)).values('header', 'content').order_by('-time_post')
    qs_emails = User.objects.all().values('email')
    email_list = []
    for email in qs_emails:
        email_list.append(email['email'])

    html_content = render_to_string(
        'send_last_news.html',
        {'post': qs_post}
    )
    msg = EmailMultiAlternatives(
        subject='Тест.Здравствуй! Вот список новостей за прошедшую неделю!',
        body=f'{qs_post}',
        from_email='egorkabox@yandex.ru',
        to=email_list,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

