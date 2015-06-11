# coding: utf-8
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import itertools
import logging
import os
import re
import sha
from StringIO import StringIO
import urllib

from mongoengine import *
import connect_redis


class Link(Document):
    url = URLField(required=True)
    tags = ListField(StringField(required=True, max_length=20), required=True)
    published_in = DateTimeField()
    views = LongField(min_value=0, max_value=None, default=0)
    text = StringField(max_length=10240)
    revised = BooleanField()
    reported = BooleanField()
    blocked = BooleanField()
    errored = BooleanField()

    @staticmethod
    def not_published():
        return Link.objects(published_in=None, revised=True, reported=None, blocked=None, errored=None)

    @staticmethod
    def get_links(adate):
        date_midnight = adate.date()
        next_day = adate.date() + timedelta(days=1)
        return Link.objects(published_in__gte=date_midnight, published_in__lt=next_day, blocked=None, errored=None)

    @staticmethod
    def increment_views(link_id):
        Link.objects(id=link_id).update_one(inc__views=1)
        link = Link.objects.get(id=link_id)
        Tag.objects(name__in=link.tags).update_one(inc__views=1)

    def publish(self):
        self.published_in = datetime.now()
        self.save()
        for tag in self.tags:
            Tag.objects.get_or_create(name=tag)

    def async_increment_views(self):
        queue = connect_redis.default_queue()
        queue.enqueue_call(func='app.tasks.increment_views', args=(self.id,))


class Tag(Document):
    name = StringField(required=True, max_length=20)
    views = LongField(min_value=0, max_value=None, default=0)

    @staticmethod
    def increment_views(tag_name):
        Tag.objects(name=tag_name).update_one(inc__views=1)

    def get_links(self):
        return Link.objects(tags=self.name)
