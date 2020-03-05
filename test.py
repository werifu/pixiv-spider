import unittest
from main import get_ok_img_url

class TestRe(unittest.TestCase):

    def test_get_img_url(self):
        self.assertEqual(get_ok_img_url())