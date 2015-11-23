import unittest
from client import RhiziAPIClient

class TestRhiziAPIClient(unittest.TestCase):

    def setUp(self):
        self.client = RhiziAPIClient("http://localhost:8080")

    def test_make_url(self):
        self.assertRaises(ValueError, lambda : self.client.make_url("/start-with-slash") )
        self.assertRaises(ValueError, lambda : self.client.make_url("http://rhizi.com/api") )
