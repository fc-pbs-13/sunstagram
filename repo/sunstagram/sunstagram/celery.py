from __future__ import absolute_import, unicode_literals

import os
from time import sleep

from celery import Celery, shared_task

# set the default Django settings module for the 'celery' program.
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sunstagram.settings.dev')

# app = Celery('celery_test', broker='redis://192.168.8.129:6379/0')
app = Celery('sunstagram', broker='redis://localhost:6379/0')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# @shared_task
# def send_email_async():
#     print('send_email called')
#     send_mail(
#         'Celery call email(User)',
#         'User created!',
#         'hsw0905@gmail.com',
#         ['hsw0905@gmail.com'],
#         fail_silently=False,
#     )


