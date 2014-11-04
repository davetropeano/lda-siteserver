import requests, json, jwt, pytest
#from rdf_json import RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder

def test_server_running():
    assert do_get_test("http://localhost:3001/")

def test_account_get():
    assert do_get_test("http://localhost:3001/account")

def test_ac_get():
    assert do_get_test("http://localhost:3001/ac")

def test_mt_get():
    assert do_get_test("http://localhost:3001/mt")

def do_get_test(url):
    r = requests.get(url, headers={}, verify=False)
    print "status code: %s" % r.status_code
    print r.text
    if r.status_code != 200:
        return False
    return True

