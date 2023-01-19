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
def mass_sender(sender, instance, action, **kwargs):
    if action == "post_add":
        categories = instance.category.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers_email_list = []
        for subscr in subscribers:
            subscribers_email_list.append(subscr.email)

        send_mail(
            subject=f'Hi {subscr.username} we have some news for you!',
            message=f'{instance.text}',
            from_email='CamcoHKappacko@yandex.ru',
            recipient_list=subscribers_email_list
        )

        # send_mail(
        #     subject=f'Hi we have some news for you!',
        #     message=f'{instance.text}',
        #     from_email='CamcoHKappacko@yandex.ru',
        #     recipient_list=['qualitya039@gmail.com']
        # )

        # categories = instance.category.all()
        # #наполняем список подписчиков категорий добавленной статьи
        # subscribers = []
        # for category in categories:
        #     subscribers += category.subscribers.all()
        #
        # subscribers_email_list = []
        # for subscr in subscribers:
        #     subscribers_email_list.append(subscr.email)
        #
        # send_email_notif(instance.preview(), instance.pk, instance.title, subscribers_email_list)