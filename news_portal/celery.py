import os
from celery import Celery
from celery.schedules import crontab
#import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_newsletter': {
        'task': 'news.tasks.weekly_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'news.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }

# app.conf.beat_schedule = {
#     'action_every_50_seconds': {
#         'task': 'news.tasks.weekly_newsletter',
#         'schedule': 50,
# #        'args': (5,),
#     },
# }