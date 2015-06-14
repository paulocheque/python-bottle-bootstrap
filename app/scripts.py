import re

from app.models import *


def add_link(string, save=False):
    blocks = string.strip().split('\n')
    url = blocks[0].split('src="')[1].split('" ')[0]
    tags = map(lambda s: s.strip(), blocks[1].split(','))
    text = blocks[2].strip()
    link = Link(url=url, tags=tags, text=text)
    if save:
        link.save()
    return link


def add_links(string, save=False):
    links = []
    blocks = string.split('\n\n')
    for block in blocks:
        link = add_link(block, save=save)
        links.append(link)
    return links
