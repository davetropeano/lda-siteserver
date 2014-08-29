import sys
sys.path.append('../lda')
sys.path.append('../../lda-serverlib')
sys.path.append('../../lda-serverlib/logiclibrary')
sys.path.append('../../lda-serverlib/mongodbstorage')
sys.path.append('../../lda-clientlib/python')
sys.path.append('../../lda-clientlib/python/test')
sys.path.append('../src')
sys.path.append('../test')

import test_utils
import requests, json, jwt
from rdf_json import URI, BNode
from base_constants import RDF, DC, AC, AC_ALL, ADMIN_USER, CE, VCARD, FOAF, ANY_USER, AC_T, AC_R, AC_C, AC_D, AC_W, AC_X
import pprint
pp = pprint.PrettyPrinter(indent=4)

HS_HOSTNAME = 'localhost:3005'

task_container_url = 'http://%s/task' % HS_HOSTNAME
userinfo_container_url = 'http://%s/userinfo' % HS_HOSTNAME
ac_container_url = 'http://%s/ac' % HS_HOSTNAME
account_container_url = 'http://%s/account' % HS_HOSTNAME

SHARED_SECRET = 'our little secret'
encoded_signature = jwt.encode({'user': ADMIN_USER}, SHARED_SECRET, 'HS256')

POST_HEADERS = {
    'Content-type': 'application/rdf+json+ce', 
    'Cookie': 'SSSESSIONID=%s' % encoded_signature, 
    'ce-post-reason': 'ce-create' 
    }

PUT_HEADERS = {
    'Content-type': 'application/rdf+json+ce', 
    'Cookie': 'SSSESSIONID=%s' % encoded_signature
    }
    
POST_ACTION_HEADERS = {
    'Content-type': 'application/rdf+json+ce', 
    'Cookie': 'SSSESSIONID=%s' % encoded_signature, 
    }
    
PATCH_HEADERS = {
    'Content-type': 'application/json', 
    'Cookie': 'SSSESSIONID=%s' % encoded_signature, 
    }

GET_HEADERS = {
    'Accept': 'application/rdf+json+ce', 
    'Cookie': 'SSSESSIONID=%s' % encoded_signature, 
    } 

DELETE_HEADERS = {
    'Cookie': 'SSSESSIONID=%s' % encoded_signature, 
    } 

def test_get_anon():
	r = requests.get("http://localhost:3005/ac", headers={}, verify=False)
	print r.text
	if r.status_code != 200:
		return False
	return True

def test_post_anon():
	#raise Exception("not yet implimented")
	return True

