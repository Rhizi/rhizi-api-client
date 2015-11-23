import requests
import random
import logging

logging.basicConfig()
log = logging.getLogger('rhizi-client')

def set_debugging():
    log.setLevel(logging.DEBUG)

class RhiziAPIClient(object):

    def __init__(self, base_url, email_address=None, password=None):
        self.base_url = base_url
        self.session = requests.session()

        log.debug("Init API at %s", base_url)

        # user log in if credentials are present
        if email_address is not None and password is not None:
            self.user_login(email_address, password)

    def make_url(self, path):
        if path[0] == "/" : raise ValueError("URL path should not start with /")
        if path[0:4] == "http" : raise ValueError("URL path should contains only path no http://'). Already : %s"%self.base_url)

        if path == "login" :
            return self.base_url + "/login"
        elif path == "signup":
            return self.base_url + "/signup"
        else :
            return self.base_url+"/api/"+path

    def make_request(self, method, path, data):
        assert method in ["POST", "GET", "DELETE"]
        assert type(data) is dict

        # make API url
        req_url = self.make_url(path)

        if method == "POST":
            log.debug( "%s API call : %s", method, req_url)
            # send request
            r = self.session.post(req_url, json=data)

            # handle 403 error
            if r.status_code == 403 :
                log.error("403 Unauthorized request")
                raise ValueError("403 Unauthorized request")
            return r

    def user_register(email_address, first_name, last_name, pw_plaintxt, rz_username):
        """POST register a new user"""
        payload = {}
        payload["email_address"]=email_address
        payload["first_name"]=first_name
        payload["last_name"]=last_name
        payload["pw_plaintxt"]=pw_plaintxt
        payload["rz_username"]=rz_username

        signup_url = make_url("signup")
        print signup_url

    def user_login(self, email_address, password):
        """POST login user"""
        payload = {}
        payload["email_address"]=email_address
        payload["password"]=password

        r = self.make_request("POST", "login", data=payload)
        assert r.status_code == 201
        log.debug("sucessfully logged in with user : %s", email_address)
        return r.json()

    def create_node(self, rzdoc_name, name, id=str(random.getrandbits(32)), labels=[]):
        assert type(labels) is list
        assert type(id) is str
        assert type(name) is str
        assert type(rzdoc_name) is str

        # create node object
        node =  {}
        node["name"] = name
        node["id"] = id
        node["__label_set"] = []

        # parse JSON data
        topo_diff = { "node_set_add" : [ node ]  }
        payload = { "rzdoc_name" : rzdoc_name, "topo_diff" : topo_diff}

        r = self.make_request("POST", "rzdoc/diff-commit__topo", data=payload)
