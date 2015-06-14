# coding: utf-8
from datetime import datetime, timedelta

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
from .tasks import *
from .utils import *


# Templates

def template(name='', data={}):
    response.content_type = 'text/html; charset=utf-8'
    return MakoTemplate(name=name, lookup=['./templates/']).render(data,
                        default_filters=['decode.utf8'],
                        output_encoding='utf-8')


@get('/')
def handler_index():
    # langs = simple_langs(request.headers.get('Accept-Language'))
    return template(name='index.html', data={'date': datetime.today().date()})


@get('/tags')
def handler_tags():
    return template(name='tags.html')


# Core API

@get('/api/v1/links/<year:int>/<month:int>/<day:int>')
def api_links_of_the_day(year, month, day):
    '''
    http GET http://localhost:8000/api/v1/links/2015/06/11
    '''
    response.content_type = 'application/json'
    currentDay = datetime(year, month, day)
    nextDay = datetime(year, month, day) + timedelta(days=1)
    lastDay = datetime(year, month, day) - timedelta(days=1)
    links = Link.get_links(currentDay)
    return {
        'links': links.to_json(),
        'currentDay': currentDay.isoformat(),
        'nextDay': nextDay.isoformat(),
        'lastDay': lastDay.isoformat(),
        'lastUpdate': lastDay.isoformat(), # FIXME
        'nextUpdate': nextDay.isoformat(), # FIXME
    }


@get('/api/v1/links/<tag_name>')
def api_links(tag_name):
    '''
    http GET http://localhost:8000/api/v1/links/a
    '''
    response.content_type = 'application/json'
    tag = Tag.objects.get(name=tag_name)
    links = tag.get_links()
    return links.to_json()


@get('/api/v1/tags')
def api_tags():
    '''
    http GET http://localhost:8000/api/v1/tags
    '''
    response.content_type = 'application/json'
    return {
        'tags': Tag.objects.order_by('name').to_json(),
        'languages': Tag.languages(),
    }


@post('/api/v1/link/<link_id>/view')
def api_add_link_view(link_id):
    '''
    http -f POST http://localhost:8000/api/v1/link/1/view
    '''
    response.content_type = 'application/json'
    Link.increment_views(link_id)
    # link = Link.objects.get(id=link_id)
    # link.async_increment_views()
    return json.dumps({'msg': 'ok'})

# Admin

@post('/api/v1/link')
def api_add_link():
    '''
    http -f POST http://localhost:8000/api/v1/link "Authorization:Token nice" url="http://google.com" tags="a,b,c" text="text"
    http -f POST http://localhost:8000/api/v1/link url="http://google.com" tags="a,b,c" text="text"
    '''
    response.content_type = 'application/json'
    token = request.get_header('Authorization', 'Token ').split(' ')[1]
    revised = True if token == 'nice' else None
    url = request.params.get('url')
    tags = request.params.get('tags').split(',')
    text = request.params.get('text')
    link, created = Link.objects.get_or_create(url=url, defaults=dict(tags=tags, text=text, revised=revised))
    if not created:
        response.status = 409
        link.text = text
        link.tags.extend(tags)
        link.save()
        return json.dumps({'msg': 'Link already exists. Link updated.'})
    else:
        if revised:
            return json.dumps({'msg': 'link has been added and revised'})
        else:
            return json.dumps({'msg': 'link has been added and it is pending'})


@post('/api/v1/link/publish')
def api_publish():
    '''
    http -f POST http://localhost:8000/api/v1/link/publish "Authorization:Token nice"
    '''
    response.content_type = 'application/json'
    token = request.get_header('Authorization', 'Token ').split(' ')[1]
    admin = True if token == 'nice' else None
    if admin:
        publish_new_link()
        return json.dumps({'msg': 'Published'})
    else:
        return json.dumps({'msg': ''})


@get('/api/v1/report')
def api_report():
    '''
    http GET http://localhost:8000/api/v1/report "Authorization:Token nice"
    '''
    response.content_type = 'application/json'
    token = request.get_header('Authorization', 'Token ').split(' ')[1]
    admin = True if token == 'nice' else None
    if admin:
        return json.dumps(report())
    else:
        return json.dumps({'msg': ''})

# User

@post('/api/v1/link/<id>/favorite')
def api_toggle_favorite(id):
    '''
    http -f POST http://localhost:8000/api/v1/link/1/favorite
    '''
    response.content_type = 'application/json'
    return json.dumps([])

# Static

@get('/static/<filepath:path>')
def handler_server_static(filepath):
    return static_file(filepath, root='./static')
