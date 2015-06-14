import unittest

from app.scripts import *


class MyTests(unittest.TestCase):
    def test_add_link(self):
        s = '''
        <iframe src="google.com" frameborder=0 width=510 height=400 scrolling=no></iframe>
        tag1 , tag2,tag3,tag4 ,tag5
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis quam ex, faucibus vitae ex a,
        '''
        link = add_link(s)
        self.assertEquals('google.com', link.url)
        self.assertEquals(['tag1', 'tag2', 'tag3', 'tag4', 'tag5'], link.tags)
        self.assertEquals(True, link.text.startswith('Lorem ipsum dolor sit amet, consectetur'))

    def test_add_links(self):
        s = '''
        <iframe src="google1.com" frameborder=0 width=510 height=400 scrolling=no></iframe>
        tag1 , tag2,tag3,tag4 ,tag5
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis quam ex, faucibus vitae ex a,

        <iframe src="google2.com" frameborder=0 width=510 height=400 scrolling=no></iframe>
        tag1 , tag2,tag3,tag4 ,tag5
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis quam ex, faucibus vitae ex a,


        <iframe src="google3.com" frameborder=0 width=510 height=400 scrolling=no></iframe>
        tag1 , tag2,tag3,tag4 ,tag5
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis quam ex, faucibus vitae ex a,
        '''
        links = add_links(s)
        self.assertEquals(3, len(links))
