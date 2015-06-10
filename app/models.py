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


class User(Document):
    SOCIAL_CHOICES = ()
    COUNTRY_CHOICES = ()

    email = EmailField(required=True, max_length=1024)
    password = StringField(max_length=1024) # social login
    secret_key = StringField(required=True, max_length=1024)
    admin = BooleanField()

    username = StringField(required=False)
    social = StringField(required=False, choices=SOCIAL_CHOICES, max_length=2)
    country = StringField(required=False, choices=COUNTRY_CHOICES)
    gender = StringField()
    registered_on = DateTimeField(required=True, default=datetime.utcnow)

    @classmethod
    def authenticate(cls, email, password):
        if password:
            pw = User.encrypt_password(password)
            return User.objects(email=email, password=pw)
        return []

    @classmethod
    def encrypt_password(cls, password):
        return sha.sha(password).hexdigest()

    @classmethod
    def generate_secret_key(cls):
        return os.urandom(24).encode('base64').strip()

    @classmethod
    def is_valid_password(cls, password):
        if not password: return False
        if len(password) < 10 or len(password) > 1024: return False
        if re.match('.*\s+', password): return False
        if not re.match('.*[a-z]+', password): return False
        if not re.match('.*[A-Z]+', password): return False
        if not re.match('.*[0-9]+', password): return False
        if not re.match('.*[!@#$%&*()_+-={}|/?;:,.<>\\\[\]]+', password): return False
        return True

    def pre_save(self, encrypt_pass=False):
        created = self.id is None
        if encrypt_pass:
            self.validate_password() # validate only for non-social logins
            self.password = User.encrypt_password(self.password)
        if not self.secret_key:
            self.secret_key = User.generate_secret_key()

    def save(self, encrypt_pass=False, **kwargs):
        self.pre_save(encrypt_pass=encrypt_pass)
        super(User, self).save(**kwargs)

    def get_or_create(encrypt_pass=False, write_concern=None, auto_save=True, *q_objs, **query):
        self.pre_save(encrypt_pass=encrypt_pass)
        return super(User, self).get_or_create(write_concern=write_concern, auto_save=auto_save, *q_objs, **query)

    def validate_password(self): # it must be called before encrypting the password
        if not User.is_valid_password(self.password):
            errors = {}
            print(self.password)
            msg = "Invalid password. It must have at least 10 chars, 1 lower case, 1 upper case, 1 number, 1 symbol."
            errors['password'] = ValidationError(msg, field_name='password')
            raise ValidationError('ValidationError', errors=errors)

    def change_password(self, current_password, new_password):
        errors = {}
        if User.encrypt_password(current_password) != self.password:
            errors['password'] = ValidationError('The current password is wrong', field_name='password')
        if current_password == new_password:
            errors['password'] = ValidationError('New password must not be the same as the old one', field_name='password')
        if errors:
            raise ValidationError('ValidationError', errors=errors)
        self.password = new_password
        self.save(encrypt_pass=True)

    def update_country(self, ip):
        import connect_redis # import to connect to redis
        from .tasks import update_country
        queue = connect_redis.default_queue()
        queue.enqueue(update_country, self.id, ip)

    def send_email(self, subject, message):
        send_email(self.email, subject, message)


class MyDoc(Document):
    email = EmailField(required=True)
    name = StringField()
    tags = ListField(StringField(max_length=20))

    # address = EmbeddedDocumentField(Address)
    # phone = EmbeddedDocumentField(Phone)
    # credit_card = EmbeddedDocumentField(CreditCard)
    # addresses = ListField(EmbeddedDocumentField(Address), required=False)
    # phones = ListField(EmbeddedDocumentField(Phone), required=False)
    # credit_cards = ListField(EmbeddedDocumentField(CreditCard), required=False)

    # Internal
    slug = StringField()
    qr_code = ImageField(size=(256,256,False))
    creation_date = DateTimeField(default=datetime.utcnow)
    update_date = DateTimeField(default=datetime.utcnow)

    def save(self, **kwargs):
        self.tags = taggify(self.tags)
        self.slug = slugify(self.name)
        if not self.qr_code:
            generate_qrcode(self.qr_code, self.url())
        self.update_date = datetime.now()
        return super(MyDoc, self).save(**kwargs)

    def url(self):
        return '{system_url}/{slug}'.format(system_url=SYSTEM_URL, slug=self.slug)

    def qrcode_url(self):
        return '{system_url}/{slug}/qrcode'.format(system_url=SYSTEM_URL, slug=self.slug)

    def async_task(self):
        queue = connect_redis.default_queue()
        queue.enqueue_call(func='apps.app.tasks.a_task', args=(None,))
