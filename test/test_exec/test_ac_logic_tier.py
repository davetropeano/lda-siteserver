import sys
sys.path.append('../../../lda-serverlib')
sys.path.append('../../../lda-serverlib/logiclibrary')
sys.path.append('../../../lda-serverlib/mongodbstorage')
sys.path.append('../../../lda-clientlib/python')
sys.path.append('../../../lda-clientlib/python/test')
sys.path.append('../../src')
sys.path.append('../../ test')

import test_utils
import requests, json, jwt
from rdf_json import URI, BNode, RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder
from base_constants import RDF, DC, AC, AC_ALL, ADMIN_USER, CE, VCARD, FOAF, ANY_USER, AC_T, AC_R, AC_C, AC_D, AC_W, AC_X
import pprint
pp = pprint.PrettyPrinter(indent=4)

TEST_USER = 'http://ibm.com/ce/user/test'
HS_HOSTNAME = 'localhost:3001'
ac_container_url = 'http://%s/ac' % HS_HOSTNAME
account_container_url = 'http://%s/account' % HS_HOSTNAME

def make_headers(type='GET', user=None, password=None,modificationCount=None):
    if type not in ('GET', 'POST', 'PATCH', 'DELETE'):
        raise Exception('invalid header type')        
    
    header = {}    
    
    if user == ADMIN_USER: 
        pass
    if user is not None:
        password = 'our little secret'
        encoded_signature = jwt.encode({'user': user}, password, 'HS256')
        header.update({'Cookie': 'SSSESSIONID=%s' % encoded_signature})
    
    if type == 'GET':
        header.update({'Accept': 'application/rdf+json+ce'})
    elif type == 'POST':
        header.update({'Content-type': 'application/rdf+json+ce'})
        #this is something about POST Action
        header.update({'ce-post-reason': 'ce-create'})
    elif type == 'PATCH':
        header.update({'Content-type': 'application/rdf+json+ce'})
        header.update({'CE-ModificationCount': modificationCount})
    
    return header

def test_basic_rest():
    container_basic_rest_test(ac_container_url)

def container_basic_rest_test(container_url):
    # test post
    body = {
        '' : {
            RDF+'type': URI(RDF+'test'),
            DC+'title': 'test post'
            }
        }
    headers = make_headers('POST', ADMIN_USER)
    r = requests.post(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 201
    r_doc = RDF_JSON_Document(r)
    assert r_doc[r_doc.default_subject()][DC+'title'] == 'test post'

    # patch
    body = {
        r_doc.default_subject() : {
            DC+'title': 'test patch'
            }
        }
    headers = make_headers('PATCH', ADMIN_USER,modificationCount=0)
    r = requests.patch(r_doc.default_subject(), headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    print r.text
    assert r.status_code == 200

    # test get
    body = {}
    headers = make_headers('GET', ADMIN_USER)
    r = requests.get(r_doc.default_subject(), headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 200
    r_doc = RDF_JSON_Document(r)
    assert r_doc[r_doc.default_subject()][DC+'title'] == 'test patch'

    # delete
    body = {}
    headers = make_headers('DELETE', ADMIN_USER)
    r = requests.delete(r_doc.default_subject(), headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 200

    body = {}
    headers = make_headers('GET', ADMIN_USER)
    r = requests.get(r_doc.default_subject(), headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 404


def test_get_as_anon():
    headers = make_headers('GET')
    body = {}
    r = requests.get(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    print r.text
    assert r.status_code == 200

def test_post_as_anon():    
    headers = make_headers('POST')
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
    headers = make_headers('POST',ADMIN_USER)
    r = requests.post(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    return r

def test_post_as_user():
    pass
    # TODO: post to ac with TEST_USER

# this is for working with tests while building them
if __name__ == "__main__":    
    test_get_as_anon()    
    pass