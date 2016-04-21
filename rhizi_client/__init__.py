import requests
import random
import logging
import sys


logging.basicConfig()
log = logging.getLogger('rhizi-client')


def set_debugging():
    log.setLevel(logging.DEBUG)

python2 = sys.version_info[0] == 2


if python2:
    def string_to_unicode(s):
        if isinstance(s, unicode):
            return s
        return s.decode('utf-8')
else:
    string_to_unicode = str
    unicode = str


# TODO - isn't this in urllib2 somewhere?
if not python2:
    bytes_ord = lambda x: x
    bytes_chr = chr
else:
    bytes_ord = ord
    bytes_chr = lambda x: x


def urlescape(s):
    b = string_to_unicode(s).encode('utf-8')
    return ''.join('%{:02x}'.format(bytes_ord(x)) if bytes_ord(x) > 128 else bytes_chr(x) for x in b)


class RhiziAPIClient(object):

    def __init__(self, base_url, email_address=None, password=None, debug=False):
        self.base_url = base_url
        self.session = requests.session()
        if debug:
            set_debugging()

        log.debug("Init API at %s", base_url)

        # user log in if credentials are present
        if email_address is not None and password is not None:
            self.user_login(email_address, password)

    def make_url(self, path):
        if path[0] == "/" : raise ValueError("URL path should not start with /")
        if path[0:4] == "http" : raise ValueError("URL path should contains only path no http://'). Already : %s"%self.base_url)

        path = urlescape(path)

        if path == "login" :
            return self.base_url + "/login"
        elif path == "signup":
            return self.base_url + "/signup"
        else :
            return "{}/api/{}".format(self.base_url, path)

    def make_request(self, method, path, data):
        assert method in ["POST", "GET", "DELETE"]
        assert type(data) is dict

        # make API url
        req_url = self.make_url(path)
        log.debug( "%s API call : %s %s", method, req_url, str(data))

        if method == "POST":
            r = self.session.post(req_url, json=data)
        elif method == "DELETE":
            r = self.session.delete(req_url, json=data)

        log.debug( "%s : %s", r.status_code, r.text)

        if r.status_code == 403 : # handle 403 error
            log.error("403 Unauthorized request")
            raise ValueError("403 Unauthorized request")
        return r

    def user_register(self, email_address, pw_plaintxt, rz_username, first_name, last_name):
        """POST register a new user"""

        payload = {}
        payload["email_address"]=email_address
        payload["first_name"]=first_name
        payload["last_name"]=last_name
        payload["pw_plaintxt"]=pw_plaintxt
        payload["rz_username"]=rz_username

        signup_url = self.make_request("POST", "signup", payload)

    def user_login(self, email_address, password):
        """POST login user"""
        payload = {}
        payload["email_address"]=email_address
        payload["password"]=password

        r = self.make_request("POST", "login", data=payload)
        assert r.status_code == 200
        log.debug("sucessfully logged in with user : %s", email_address)

    def rz_doc_create(self, doc_name):
        """Create a new Rz-Doc"""
        assert type(doc_name) is unicode
        log.debug("Creating new rz-doc : %s", doc_name)
        r = self.make_request("POST", 'rzdoc/' + doc_name + '/create', {})
        return r

    def rz_doc_clone(self, doc_name):
        """Clone an existing Rz-Doc"""
        assert type(doc_name) is unicode
        log.debug("cloning existing rz-doc : %s", doc_name)
        r = self.make_request("POST", 'rzdoc/clone', {"rzdoc_name" : doc_name})
        return r

    def rz_doc_delete(self, doc_name):
        """Delete a new Rz-Doc"""
        assert type(doc_name) is unicode
        r = self.make_request("DELETE", 'rzdoc/' + doc_name + '/delete', {})
        log.debug("Deleted Rz-doc : %s", doc_name)
        return r

    def rz_doc_search(self, doc_name):
        """Search a Rz-Doc by name"""
        assert type(doc_name) is unicode
        log.debug("Search Rz-doc : %s", doc_name)
        r = self.make_request("POST", 'rzdoc/search', {'search_query' : doc_name})
        return r

    def node_create_one(self, rzdoc_name, name, node_id=None, labels=None):
        """Create a single node"""

        if node_id is None:
            node_id = str(random.getrandbits(32))
        if labels is None:
            labels = ["Type"]

        assert type(labels) is list
        assert type(node_id) is str
        assert type(name) is unicode
        assert type(rzdoc_name) is unicode

        # create node object
        node =  {}
        node["name"] = name
        node["id"] = node_id
        node["__label_set"] = labels

        # parse JSON data
        topo_diff = { "node_set_add" : [ node ]  }
        payload = { "rzdoc_name" : rzdoc_name, "topo_diff" : topo_diff}

        r = self.make_request("POST", "rzdoc/diff-commit__topo", data=payload)
        return r

    def node_create(self, rzdoc_name, nodes):
        """Create multiple nodes at once"""
        # check params
        assert type(rzdoc_name) is unicode
        assert type(nodes) is list
        for node in nodes:
            assert type(node["label"]) is list
            assert type(node["id"]) is str
            assert type(node["name"]) is unicode
            node["__label_set"] = node["label"]
            del(node["label"])

        # parse JSON data
        topo_diff = { "node_set_add" : nodes  }
        payload = { "rzdoc_name" : rzdoc_name, "topo_diff" : topo_diff}

        r = self.make_request("POST", "rzdoc/diff-commit__topo", data=payload)
        return r

    def node_delete(self, rzdoc_name, name):
        raise NotImplementedError

    def edge_create_one(self, rzdoc_name, nodeA_id, nodeB_id, id=str(random.getrandbits(32)), relationships=None):
        """Create an edge giving two existing nodes"""

        if relationships == None or len(relationships) != 1:
            raise Exception("must supply a single relationship, as supported currently by neo4j (in the way rhizi uses it)")

        # check params
        assert type(rzdoc_name) is unicode
        assert type(nodeA_id) is str
        assert type(nodeB_id) is str
        assert type(relationships) is list

        # make link
        link = {}
        link["id"] = id
        link["__dst_id"] = nodeA_id
        link["__src_id"] = nodeB_id
        link["__type"] = relationships

        # payload
        topo_diff = { "link_set_add" : [ link ]  }
        payload = { "rzdoc_name" : rzdoc_name, "topo_diff" : topo_diff}

        r = self.make_request("POST", "rzdoc/diff-commit__topo", data=payload)
        return r

    def edge_create(self, rzdoc_name, edges):
        """Create edges giving a list of dict {__src_id:"", __dst_id:"", __type:[]}"""

        # check params
        assert type(edges) is list
        assert type(rzdoc_name) is unicode
        for edge in edges:
            assert type(edge) is dict
            assert type(edge["__src_id"]) is str
            assert type(edge["__dst_id"]) is str
            assert type(edge["__type"]) is list
            try :
                assert type(edge["id"]) is str
            except KeyError:
                edge["id"] = str(random.getrandbits(32))

        # payload
        topo_diff = { "link_set_add" : edges   }
        payload = { "rzdoc_name" : rzdoc_name, "topo_diff" : topo_diff}

        r = self.make_request("POST", "rzdoc/diff-commit__topo", data=payload)
        return r

    # attributes
    def edge_update_attr_single(self, rzdoc_name, edge_id, attrs):
        """Update attributes of an edge"""
        # check params
        assert type(attrs) is dict
        assert type(node_id) is str
        assert type(rzdoc_name) is unicode

        # parse data
        attr_diff = {}
        attr_diff["__type_link"] = {
            edge_id : {
                "__attr_write"  : attrs,
            }
        }
        payload = { "rzdoc_name" : rzdoc_name, "attr_diff" : attr_diff}

        r = self.make_request("POST", "rzdoc/diff-commit__attr", data=payload)
        return r

    def edge_update_attr(self, rzdoc_name, edge_attrs):
        """Update attributes of edges"""
        # check params
        assert type(rzdoc_name) is unicode
        assert type(edge_attrs) is dict
        for edge_id in edge_attrs :
            assert type(edge_id) is str
            assert type(edge_attrs[edge_id]) is dict

        attrs = { id : { "__attr_write" : edge_attrs[id]} for id in edge_attrs }
        log.debug(attrs)

        # parse data
        attr_diff = {}
        attr_diff["__type_link"] = attrs

        payload = { "rzdoc_name" : rzdoc_name, "attr_diff" : attr_diff}

        r = self.make_request("POST", "rzdoc/diff-commit__attr", data=payload)
        return r

    def node_update_attr_single(self, rzdoc_name, node_id, attrs):
        """Update attributes of a node"""
        # check params
        assert type(attrs) is dict
        assert type(node_id) is str
        assert type(rzdoc_name) is unicode

        # parse data
        attr_diff = {}
        attr_diff["__type_node"] = {
            node_id : {
                "__attr_write"  : attrs,
            }
        }
        payload = { "rzdoc_name" : rzdoc_name, "attr_diff" : attr_diff}

        r = self.make_request("POST", "rzdoc/diff-commit__attr", data=payload)
        return r

    def node_update_attr(self, rzdoc_name, node_attrs):
        """Update attributes of an edge"""
        # check params
        assert type(rzdoc_name) is unicode
        for node_id in node_attrs :
            assert type(node_id) is str
            assert type(node_attrs[node_id]) is dict

        # parse data
        attrs = { id : { "__attr_write" : node_attrs[id]} for id in node_attrs }
        log.debug(attrs)

        attr_diff = {}
        attr_diff["__type_node"] = attrs
        payload = { "rzdoc_name" : rzdoc_name, "attr_diff" : attr_diff}
        r = self.make_request("POST", "rzdoc/diff-commit__attr", data=payload)
        return r
