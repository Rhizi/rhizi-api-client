import unittest
from client import RhiziAPIClient, set_debugging

class TestRhiziAPIClient(unittest.TestCase):

    def setUp(self):

        # constant
        self.rz_doc_name = "Test"
        self.user_email = "tester@test.com"
        self.user_password = "password"

        # init client
        self.client = RhiziAPIClient("http://localhost:8080", debug=True)

        # create a test user
        self.client.user_register(self.user_email, self.user_password, "tester", "Test", "User")
        # TODO : activate email ?

        # user login and store credentials
        self.client.user_login(self.user_email, self.user_password)

        # clean DB and create a new Test rz doc
        self.client.delete_rz_doc(self.rz_doc_name)
        self.client.create_rz_doc(self.rz_doc_name)

    def test_make_url(self):
        """URLs should be conformed, errors should be raised when passing wrong paths """
        self.assertRaises(ValueError, lambda : self.client.make_url("/start-with-slash") )
        self.assertRaises(ValueError, lambda : self.client.make_url("http://rhizi.com/api") )

    def test_create_new_doc(self):
        """API should allow creation and deleting of new documents"""
        self.assertRaises(AssertionError, lambda : self.client.create_rz_doc(12) ) # wrong type
        doc_name = "New Test Doc"
        r = self.client.create_rz_doc(doc_name)
        self.assertEqual(r.status_code, 201)
        r= self.client.search_rz_doc(doc_name)
        self.assertEqual(r.status_code, 200)
        self.assertIn(doc_name, r.text)
        r= self.client.delete_rz_doc(doc_name)
        self.assertEqual(r.status_code, 204)

    def test_node_create(self):
        """API should allow node creation"""
        self.assertRaises(AssertionError, lambda : self.client.create_node(12,"haha") )
        self.assertRaises(AssertionError, lambda : self.client.create_node("12",12) )

        id = "ID-89388"
        name="My Test Node"

        # TODO : non-authorized should raise error
        # self.assertRaises(ValueError, lambda : self.client.create_node("Test", name, id=id, labels=["Type"]) )

        r = self.client.create_node(self.rz_doc_name, name, id=id, labels=["Type"])
        self.assertEqual(r.status_code, 200)
