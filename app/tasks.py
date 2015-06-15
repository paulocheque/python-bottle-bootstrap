# coding: utf-8
from datetime import datetime, timedelta
import random

from celery.schedules import crontab
from celery.task import periodic_task

import connect_mongo # Important: Celery run this module independently
from .models import *


# BR:  00:00 - 06:00 - 12:00 - 18:00
# UTC: 21:00 - 03:00 - 09:00 - 15:00
@periodic_task(run_every=crontab(minute=0, hour='3,9,15,21'))
def publish_new_link():
    total = Link.all_not_published().count()
    if total > 0:
        index = random.randint(0, total-1) # [0, total-1]
        link = Link.all_not_published()[index]
        link.publish()
        refresh_cache()
        return True
    else:
        return False


@periodic_task(run_every=crontab(minute='*/15'))
def refresh_cache():
    # refresh cache tags
    # refresh cache last_day
    # refresh cache today
    pass


def increment_views(link_id):
    Link.increment_views(link_id)


def report():
    return {
        '# of Links': Link.objects.count(),
        '# of Not Published Links': Link.all_not_published(),
        '# of Published Links': Link.all_published().count(),
        '# of Removed Links': Link.all_removed().count(),
        '# of Reported Links': Link.all_reported().count(),
        'Top Links': ['{}: {}'.format(l.views, l.url) for l in Link.top_links()],
        '# of Tags': Tag.objects.count(),
        'Top Tags': ['{}: {}'.format(t.views, t.name) for t in Tag.top_tags()],
    }
