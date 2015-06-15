from datetime import timedelta
import logging
import os

from celery import Celery
from celery.task import periodic_task


redis_url = os.getenv('REDIS_URL', os.getenv('REDISTOGO_URL', 'redis://localhost:6379'))

celery = Celery('tasks', broker=redis_url)


# Celery Tasks
from app.tasks import *
