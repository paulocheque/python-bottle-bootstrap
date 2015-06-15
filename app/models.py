# coding: utf-8
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import itertools
import logging
import os
import random
import re
import sha
from StringIO import StringIO
import urllib

from mongoengine import *

import connect_mongo


class System(Document):
    last_update = DateTimeField()
    next_update = DateTimeField()

    def save(self, *args, **kwargs):
        # BR: 00:00 - 06:00 - 12:00 - 18:00
        # UTC: 21:00 - 03:00 - 09:00 - 15:00
        self.last_update = datetime.now()
        self.next_update = self.last_update + timedelta(hours=6)
        return super(System, self).save(*args, **kwargs)


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
    def all_not_published():
        return Link.objects(published_in=None, revised=True, reported=None, blocked=None, errored=None)

    @staticmethod
    def all_published():
        return Link.objects(published_in__ne=None, revised=True, reported=None, blocked=None, errored=None)

    @staticmethod
    def all_removed():
        return Link.objects(Q(published_in__ne=None) & (Q(blocked=True) | Q(errored=True)))

    @staticmethod
    def all_reported():
        return Link.objects(published_in__ne=None, reported__ne=None, blocked=None, errored=None)

    @staticmethod
    def top_links():
        return Link.all_published().order_by('-views')[0:10]

    @staticmethod
    def get_links(adate):
        date_midnight = adate.date()
        next_day = adate.date() + timedelta(days=1)
        links = Link.objects(published_in__gte=date_midnight, published_in__lt=next_day, blocked=None, errored=None)
        for index, link in enumerate(links):
            if link.views < 500:
                links[index].views = links[index].views + random.randint(500, 1000)
        return links

    @staticmethod
    def increment_views(link_id):
        Link.objects(id=link_id).update_one(inc__views=1)
        link = Link.objects.get(id=link_id)
        Tag.objects(name__in=link.tags).update_one(inc__views=1)

    def save(self, *args, **kwargs):
        self.tags = list(set(self.tags))
        return super(Link, self).save(*args, **kwargs)

    def publish(self):
        self.published_in = datetime.now()
        self.save()
        for tag in self.tags:
            tag, created = Tag.objects.get_or_create(name=tag)
            if created:
                tag.translate()
            tag.links += 1
            tag.save()
        s, _ = System.objects.get_or_create()
        s.save()


class Tag(Document):
    name = StringField(required=True, max_length=20) # default en
    views = LongField(min_value=0, max_value=None, default=0)
    links = LongField(min_value=0, max_value=None, default=0)
    translations = MapField(field=StringField(max_length=40))

    @staticmethod
    def top_tags():
        return Tag.objects.order_by('-views')[0:10]

    @staticmethod
    def increment_views(tag_name):
        Tag.objects(name=tag_name).update_one(inc__views=1)

    @staticmethod
    def languages():
        '''
        arabic ar
        german de
        spanish es
        english en
        french fr
        hindi hi
        italian it
        portuguese pt
        russian ru
        mandarin zh
        '''
        return sorted('ar,de,en,es,fr,hi,it,pt,ru,zh'.split(','))

    def translate(self):
        import goslate
        gs = goslate.Goslate()
        for lang in Tag.languages():
            translation = gs.translate(self.name, lang)
            self.translations[lang] = translation
        self.save()

    def get_name(self, lang=None):
        if lang and lang in self.translations:
            return self.translations[lang]
        return self.name

    def get_links(self):
        return Link.objects(tags=self.name)
