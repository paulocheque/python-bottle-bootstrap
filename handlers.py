import hashlib

from bottle import static_file
from bottle import route, post, request, response, error, redirect, template
from bottle import MakoTemplate, mako_template as template

try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

from models import *


def template(name='', data={}):
    response.content_type = 'text/html; charset=utf-8'
    return MakoTemplate(name=name, lookup=['./templates/']).render(data,
                        default_filters=['decode.utf8'],
                        output_encoding='utf-8')


@route('/')
def index():
    return template(name='index.html')


@route('/api/v1/images')
def images():
    response.content_type = 'application/json'
    return json.dumps(ImageLink.all())


@post('/save')
def save():
    response.content_type = 'text/html; charset=utf-8'
    redirect('/%s' % (''))


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')
