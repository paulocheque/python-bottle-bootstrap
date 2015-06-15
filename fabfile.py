# coding: utf-8
from __future__ import with_statement

from fabric.api import *
from fabric.colors import *
from fabric.utils import abort
from fabric.contrib.console import confirm

from fab_scripts.fabfile_heroku import *

# fab --list

from app.scripts import add_links


@task
def add():
    s = '''
    <iframe src="http://google1.com" frameborder=0 width=510 height=400 scrolling=no></iframe>
    tag1 , tag2,tag3,tag4 ,tag5
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis quam ex, faucibus vitae ex a,

    <iframe src="http://google2.com" frameborder=0 width=510 height=400 scrolling=no></iframe>
    tag1 , tag2,tag3,tag4 ,tag5
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis quam ex, faucibus vitae ex a,


    <iframe src="http://google3.com" frameborder=0 width=510 height=400 scrolling=no></iframe>
    tag1 , tag2,tag3,tag4 ,tag5
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis quam ex, faucibus vitae ex a,
    '''
    add_links(s, save=True)
