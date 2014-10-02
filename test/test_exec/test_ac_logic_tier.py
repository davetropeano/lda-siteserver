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

HS_HOSTNAME = 'localhost:3005'

ac_container_url = 'http://%s/ac' % HS_HOSTNAME
account_container_url = 'http://%s/account' % HS_HOSTNAME

def make_headers(type = 'GET', user = None,password = None):
    if type not in ('GET', 'POST', 'PATCH', 'DELETE'):
        raise Exception('invalid header type')        
    
    header = {}    
    
    if user == ADMIN_USER: 
        password = 'our little secret'    
    if user is not None:
        encoded_signature = jwt.encode({'user': user}, password, 'HS256')
        header.update({'Cookie': 'SSSESSIONID=%s' % encoded_signature})
    
    if type == 'GET':
        header.update({'Accept': 'application/rdf+json+ce'})
    elif type == 'POST':
        header.update({'Content-type': 'application/rdf+json+ce'})
        #this is something about POST Action
        header.update({'ce-post-reason': 'ce-create'})
    elif type == 'PATCH':
        header.update({'Content-type': 'application/json'})
    
    return header

def test_get_as_anon():
    headers = make_headers('GET')
    body = {}
    r = requests.get(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    print r.text
    if r.status_code != 200:
        return False
    return True

def test_post_as_anon():    
    headers = make_headers('POST')
    body = {}
    r = requests.post(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    print "status code: %s" % r.status_code
    print r.text
    if r.status_code != 401:        
        return False
    return True    

def test_post_as_admin():
    # give everyone access to create new accounts    
    body = {
        '' : {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who' : [
                URI(ANY_USER)
                ],
            AC+'may' : [ URI('#permission_1') ],
            },
        '#permission_1' : {
            AC+'do' : AC_C,
            AC+'to' : [URI(account_container_url) ]
            }
        }
    body = {}
    headers = make_headers('POST',ADMIN_USER)
    r = requests.post(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    print "status code: %s" % r.status_code
    print r.text
    if r.status_code != 201:        
        return False
    return True

def test_post_as_user():
    # give everyone access to create new accounts    
    body = {
        '' : {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who' : [
                URI(ANY_USER)
                ],
            AC+'may' : [ URI('#permission_1') ],
            },
        '#permission_1' : {
            AC+'do' : AC_C,
            AC+'to' : [URI(account_container_url) ]
            }
        }
    body = {}
    headers = make_headers('POST',ADMIN_USER)
    r = requests.post(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    print "status code: %s" % r.status_code
    print r.text
    if r.status_code != 201:        
        return False
    return True
    
# this is for working with tests while building them 
if __name__ == "__main__":    
    test_get_as_anon()    
    pass