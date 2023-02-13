from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from news_portal import settings


@receiver(m2m_changed, sender=PostCategory)
def mass_sender(sender, instance, action, **kwargs):
    if action == "post_add":
        categories = instance.category.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers_email_list = []
        for subscriber in subscribers:
            subscribers_email_list.append(subscriber.email)

        if subscribers_email_list:
            html_content = render_to_string(
                    'mailtest.html',
                    {
                        'instance': instance,
                        'subscriber': subscriber,
                        'link': f'{settings.SITE_URL}/news/{instance.id}',
                    })

            send_mail(
                subject=f'{instance.article}',
                message=f'Здравствуй {subscriber.username} Новая статья в твоём любимом разделе!!{instance.text[:200]}',
                from_email='CamcoHKappacko@yandex.ru',
                recipient_list=subscribers_email_list,
                html_message=html_content
            )

            # #получаем наш html
            # html_content = render_to_string(
            #     'mailtest.html',
            #     {
            #         'post': msg,
            #     }
            # )
            #
            # # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
            # msg = EmailMultiAlternatives(
            #     subject=f'Hi {subscriber.username} we have some news for you!',
            #     body=f'{instance.text[:200]}',  # это то же, что и message
            #     from_email='CamcoHKappacko@yandex.ru',
            #     to=subscribers_email_list,  # это то же, что и recipients_list
            # )
            # msg.attach_alternative(html_content, "text/html")  # добавляем html
            #
            # msg.send()  # отсылаем
#            print(subscribers_email_list)
#            print(instance)
