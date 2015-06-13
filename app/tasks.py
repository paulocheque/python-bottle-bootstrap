# coding: utf-8
from datetime import datetime, timedelta
import random

from .models import *


def publish_new_link(): # it should run daily at 9/15/21 UTC
    total = Link.all_not_published().count()
    if total > 0:
        index = random.randint(0, total)
        link = Link.all_not_published()[index]
        link.publish()
        refresh_cache()


def refresh_cache(): # it should run every 15minutes
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
