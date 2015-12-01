import unittest
from rhizi_client import RhiziAPIClient, set_debugging
import json

class TestRhiziAPIClient(unittest.TestCase):

    @classmethod
    def setUpClass(self):

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
        self.client.rz_doc_delete(self.rz_doc_name)
        self.client.rz_doc_create(self.rz_doc_name)

    def test_make_url(self):
        """URLs should be conformed, errors should be raised when passing wrong paths """
        self.assertRaises(ValueError, lambda : self.client.make_url("/start-with-slash") )
        self.assertRaises(ValueError, lambda : self.client.make_url("http://rhizi.com/api") )

    def test_rz_doc_create_delete_search(self):
        """API should allow creation and deleting of new documents"""
        self.assertRaises(AssertionError, lambda : self.client.rz_doc_create(12) ) # wrong type

        doc_name = "New Test Doc"
        r= self.client.rz_doc_delete(doc_name)

        r = self.client.rz_doc_create(doc_name)
        self.assertEqual(r.status_code, 201)

        # search
        r= self.client.rz_doc_search(doc_name)
        self.assertEqual(r.status_code, 200)
        self.assertIn(doc_name, r.text)

        # clone
        r_clone= self.client.rz_doc_clone(doc_name)
        self.assertEqual(r_clone.status_code, 200)
        resp = json.loads(r_clone.text)
        # print resp
        self.assertEqual(None, resp["error"])

        r= self.client.rz_doc_delete(doc_name)
        self.assertEqual(r.status_code, 204)

    def test_node_create(self):
        """API should allow node creation"""
        self.assertRaises(AssertionError, lambda : self.client.node_create(12,"haha") )
        self.assertRaises(AssertionError, lambda : self.client.node_create("12",12) )

        id = "ID-89388"
        name="My Test Node"

        # TODO : non-authorized should raise error
        # self.assertRaises(ValueError, lambda : self.client.node_create("Test", name, id=id, labels=["Type"]) )

        r = self.client.node_create_one(self.rz_doc_name, name, id=id, labels=["Type"])
        self.assertEqual(r.status_code, 200)

        nodes = [{"name":"nodeA", "label": ["skill"], "id":"node_01"}, {"name":"nodeB", "label": ["keyword"], "id":"node_02"}]
        r = self.client.node_create(self.rz_doc_name, nodes)
        self.assertEqual(r.status_code, 200)

    def test_node_attr_update(self):

        # create a node
        id = "ID-1"
        name="My Changing Node"
        r = self.client.node_create_one(self.rz_doc_name, name, id=id, labels=["Type"])

        # modify name
        r = self.client.node_update_attr(self.rz_doc_name, id, {"name" : "My Awesome Node","description" : "Greatest node ever." })

    def test_edge_create(self):

        nodes = [
            {"name":"John", "label": ["Person"], "id":"node_03"},
            {"name":"ELM coding", "label": ["Skill"], "id":"node_04"},
            {"name":"Video Game", "label": ["Idea"], "id":"node_05"},
            {"name":"Jacky", "label": ["Person"], "id":"node_06"},
            ]
        r = self.client.node_create(self.rz_doc_name, nodes)

        # create an edge
        self.client.edge_create_one(self.rz_doc_name, nodes[0]["id"], nodes[1]["id"], relationships=["loves"])
        self.assertEqual(r.status_code, 200)

        # multiple edges
        edges_data = [("node_03", "node_04", "is learning"),
        ("node_04", "node_05", "is used for"),
        ("node_03", "node_06", "loves"),
        ("node_06", "node_03", "hates")
        ]

        edges = [ {"__src_id" : e[0],"__dst_id" : e[1] , "__type" : [e[2]], "options": {"option" : "test"} } for e in edges_data]

        self.client.edge_create(self.rz_doc_name, edges)
        self.assertEqual(r.status_code, 200)
