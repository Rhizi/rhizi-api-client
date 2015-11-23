import requests

class RhiziAPIClient(object):

    def __init__(self, base_url):
        self.base_url = base_url

    def make_url(self, path):
        if path[0] == "/" : raise ValueError("URL path should not start with /")
        if path[0:4] == "http" : raise ValueError("URL path should contains only path no http://'). Already : %s"%self.base_url)

        return self.base_url+"/api/"+path

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
        r = requests.post(signup_url, data=payload)

    def user_login(self, email_address, password):
        """POST login user"""
        payload = {}
        payload["email_address"]=email_address
        payload["password"]=password

        # login_url = self.make_url("login")
        login_url = self.base_url + "/login"

        r = requests.post(login_url, data=payload)
        assert r.status_code == 200
        return r.json()
