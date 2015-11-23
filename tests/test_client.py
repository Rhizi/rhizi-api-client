import unittest
from client import RhiziAPIClient, set_debugging

class TestRhiziAPIClient(unittest.TestCase):

    def setUp(self):
        self.client = RhiziAPIClient("http://localhost:8080", debug=True)
        # create a test user
        self.client.user_register("tester@test.com", "password", "tester", "Test", "User")
        # TODO : activate email ?


    def test_make_url(self):
        """URLs should be conformed, errors should be raised when passing wrong paths """
        self.assertRaises(ValueError, lambda : self.client.make_url("/start-with-slash") )
        self.assertRaises(ValueError, lambda : self.client.make_url("http://rhizi.com/api") )

    def test_node_create(self):
        """should create node"""
        self.assertRaises(AssertionError, lambda : self.client.create_node(12,"haha") )
        self.assertRaises(AssertionError, lambda : self.client.create_node("12",12) )

        id = "ID-89388"
        name="My Test Node"

        # non-authorized should raise error
        self.assertRaises(ValueError, lambda : self.client.create_node("Test", name, id=id, labels=["Type"]) )

        self.client.user_login("tester@test.com", "password")
        r = self.client.create_node("Test", name, id=id, labels=["Type"])
        self.assertEqual(r.status_code, 200)
