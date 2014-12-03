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
import pytest

import pprint
pp = pprint.PrettyPrinter(indent=4)

TEST_USER = 'http://ibm.com/ce/user/test'
HS_HOSTNAME = 'hostingsite.localhost:3001'
ac_container_url = 'http://%s/ac' % HS_HOSTNAME
account_container_url = 'http://%s/account' % HS_HOSTNAME

def test_basic_crud():
    '''
    post_body = {
        '' : {
            RDF+'type': URI(CE+'Account'),
            CE+'account_id' : 'test2',
            CE+'password': 'test2',
            VCARD+'email': 'test2@us.ibm.com',
            DC+'title': 'test2 account'
            }
        }
    patch_prop = DC+'title'
    patch_val = 'updated test2 account'
    test_helper.container_crud_test(account_container_url, post_body, patch_prop, patch_val)
    '''
    create_test_account()

@pytest.fixture(scope="session")
def create_test_account():
    body = { \
        '': {
            RDF+'type': URI(CE+'Account'),
            CE+'account_id': 'test',
            CE+'password': 'test',
            VCARD+'email': 'test@us.ibm.com',
            CE+'user': URI('#owner'),
            VCARD+'adr': BNode('_:address')
            },
        '#owner' : {
            RDF+'type': URI(FOAF+'Person'),
            FOAF+'givenName': 'FName',
            FOAF+'familyName': 'LName',
            FOAF+'nick': 'NName'
            },
        '_:address' : {
            RDF+'type': URI(VCARD+'Work'),
            VCARD+'street-address': 'unknown',
            VCARD+'locality': 'Seville',
            VCARD+'region': 'Andalusia',
            VCARD+'postal-code': '00000',
            VCARD+'country-name': 'Spain'
            }
        }
    headers = test_helper.make_headers('POST')
    r = requests.post(account_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 201
    return r

# this is for working with tests while building them
if __name__ == "__main__":
    create_test_account()
    pass