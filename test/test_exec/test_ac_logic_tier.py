import sys
sys.path.append('../../../lda-serverlib')
sys.path.append('../../../lda-serverlib/logiclibrary')
sys.path.append('../../../lda-serverlib/mongodbstorage')
sys.path.append('../../../lda-clientlib/python')
sys.path.append('../../../lda-clientlib/python/test')
sys.path.append('../../src')
sys.path.append('../../ test')

import requests, json, jwt
from rdf_json import URI, BNode, RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder
from base_constants import RDF, DC, AC, AC_ALL, ADMIN_USER, CE, VCARD, FOAF, ANY_USER, AC_T, AC_R, AC_C, AC_D, AC_W, AC_X
import test_helper

import pprint
pp = pprint.PrettyPrinter(indent=4)

TEST_USER = 'http://ibm.com/ce/user/test'
HS_HOSTNAME = 'localhost:3001'
ac_container_url = 'http://%s/ac' % HS_HOSTNAME
account_container_url = 'http://%s/account' % HS_HOSTNAME

def test_basic_crud():
    test_helper.container_crud_test(ac_container_url, DC+'title', RDF+'test', 'test post', 'test patch')

def test_get_as_anon():
    headers = test_helper.make_headers('GET')
    body = {}
    r = requests.get(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    print r.text
    assert r.status_code == 200

def test_post_as_anon():    
    headers = test_helper.make_headers('POST')
    body = {}
    r = requests.post(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    print "status code: %s" % r.status_code
    print r.text
    assert r.status_code == 401

def admin_create_account_usergroup():
    # give everyone access to create new accounts
    body = {
        '' : {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who' : [
                URI(ANY_USER)
                ],
            AC+'may' : [ URI('#permission_1')],
            },
        '#permission_1' : {
            AC+'do' : AC_C,
            AC+'to' : [URI(account_container_url)]
            }
        }
    body = {}
    headers = test_helper.make_headers('POST',ADMIN_USER)
    r = requests.post(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    return r

def test_post_as_user():
    pass
    # TODO: post to ac with TEST_USER
