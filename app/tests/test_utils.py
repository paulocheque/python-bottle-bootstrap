import unittest

from app.utils import *


class UtilsTests(unittest.TestCase):
    def test_simple_langs(self):
        header = 'en-US,en;q=0.8,pt;q=0.6'
        langs = simple_langs(header)
        self.assertEquals(['en', 'pt'], langs)
