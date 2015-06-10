import hashlib

from bottle import static_file
from bottle import get, post, request, response, error, redirect, template
from bottle import MakoTemplate, mako_template as template

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

from .models import *


def template(name='', data={}):
    response.content_type = 'text/html; charset=utf-8'
    return MakoTemplate(name=name, lookup=['./templates/']).render(data,
                        default_filters=['decode.utf8'],
                        output_encoding='utf-8')

# Index

@get('/')
def index():
    return template(name='index.html')

# Core API

@get('/api/v1/links/<year>/<month>/<day>')
def links():
    response.content_type = 'application/json'
    return json.dumps([])
