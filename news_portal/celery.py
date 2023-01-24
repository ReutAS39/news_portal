import os
from celery import Celery
from celery.schedules import crontab
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'spam_weekly': {
        'task': 'news.tasks.weekly_spam',
        'schedule': crontab(hour=1, minute=0, day_of_week=1),
    },
}

# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'NewsPaper.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }