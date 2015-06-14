import unittest

import connect_mongo
from app.models import *


class ModelsTests(unittest.TestCase):
    def test_tag(self):
        tag = Tag.objects.create(name='a')
        tag.add_translation('pt', 'b')
        tag.add_translations([('en', 'c'), ('es', 'd')])
        self.assertEquals('b', tag.get_name('pt'))
        self.assertEquals('c', tag.get_name('en'))
        self.assertEquals('d', tag.get_name('es'))
        self.assertEquals('a', tag.get_name('it'))
