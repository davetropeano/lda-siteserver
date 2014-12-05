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
HS_HOSTNAME = 'hostingsite.localhost:3001'
ac_container_url = 'http://%s/ac' % HS_HOSTNAME
account_container_url = 'http://%s/account' % HS_HOSTNAME
mt_container_url = 'http://%s/mt' % HS_HOSTNAME
mt_sites_url = 'http://%s/mt/sites' % HS_HOSTNAME
mt_capabilities_url = 'http://%s/mt/capabilities' % HS_HOSTNAME


def test_basic_crud():
    headers_post = test_helper.make_headers('POST', ADMIN_USER)
    body = {
        '' : {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who' : [
                URI(ADMIN_USER)
                ],
            AC+'may' : [ URI('#permission_1') ],
            },
        '#permission_1' : {
            AC+'do' : AC_ALL,
            AC+'to' : [ URI('/'), URI('/mt/cloudsupplements'), URI('/mt/testsite') ]
            }
        }
    r = requests.post(ac_container_url, headers=headers_post, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 201

    post_body = {
        '': {
            RDF+'type': URI(CE+'Capability'),
            DC+'title': 'test capability',
            CE+'improvement_container': URI('/cat/stores'),
            CE+'improvement_type': URI('http://setupshop.me/ns#OnlineStore')
        }
    }
    patch_prop = DC+'title'
    patch_val = 'updated test capability'
    test_helper.container_crud_test(mt_capabilities_url, post_body, patch_prop, patch_val)

# this is for working with tests while building them
if __name__ == "__main__":
    test_basic_crud()
    pass