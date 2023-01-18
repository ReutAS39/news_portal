from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import PostCategory


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
# @receiver(post_save, sender=Post)
# def notify_managers_appointment(sender, instance, created, **kwargs):
#     if created:
#         subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
#     else:
#         subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'
#
#     mail_managers(
#         subject=subject,
#         message=instance.message,
#     )
#     mail_

@receiver(m2m_changed, sender=PostCategory)
def mass_sender(request, sender, instance, action, **kwargs):
    if action == "post_add":
        send_mail(
            subject=f'Hi {request.user}, we have some news for you!',
            message=f'{instance.text}',
            from_email='CamcoHKappacko@yandex.ru',
            recipient_list=['qualytya039@gmail.com']
        )