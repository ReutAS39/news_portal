from celery import shared_task
import time
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from news_portal import settings
from .models import Post, Category
from .models import PostCategory

from .signals import mass_sender
from django.core.mail import send_mail

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
# def notify_at_new_post_added(post_pk):
#     #обьект статьи
#     post = Post.objects.get(id=post_pk)
#
#     #получаем категории добавленной статьи
#     categories = post.category.all()
#
#     #наполняем список подписчиков категорий добавленной статьи
#     subscribers = []
#     for category in categories:
#         subscribers += category.subscribers.all()
#
#     subscribers_email_list = []
#     for subscr in subscribers:
#         subscribers_email_list.append(subscr.email)
#
#     send_email_notif(post.preview(), post.pk, post.title, subscribers_email_list)
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

@shared_task
def weekly_spam():
    # #Your job processing logic here...
    print('hello from job')

    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email='CamcoHKappacko@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()