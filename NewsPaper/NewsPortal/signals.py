from .models import Post
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver


@receiver(post_save, sender=Post)
def notify_post(sender, instance, created, **kwargs):
    if created:
        subject = f'У нас новая статья'
    else:
        subject = f'Что-то новое появилось на сайте'
    # mail_managers(
    #     subject=subject,
    #     message=instance.header,
    # )
    send_mail(
        subject=subject,
        message=instance.header,
        from_email='egorkabox@yandex.ru',
        recipient_list=['nurjanello@mail.ru']
    )