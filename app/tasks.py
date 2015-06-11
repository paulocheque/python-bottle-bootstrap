# coding: utf-8
from datetime import datetime, timedelta
import random

from .models import *


def publish_new_link(): # it should run daily at 9/15/21 UTC
    total = Link.not_published().count()
    if total > 0:
        index = random.randint(0, total)
        link = Link.not_published()[index]
        link.publish()
        refresh_cache()


def refresh_cache(): # it should run every 15minutes
    # refresh cache tags
    # refresh cache last_day
    # refresh cache today
    pass


def increment_views(link_id):
    Link.increment_views(link_id)
