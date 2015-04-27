import sys
sys.path.append('../../../lda-serverlib')
sys.path.append('../../../lda-serverlib/logiclibrary')
sys.path.append('../../../lda-serverlib/mongodbstorage')
sys.path.append('../../../lda-clientlib/python')
sys.path.append('../../../lda-clientlib/python/test')
sys.path.append('../../src')
sys.path.append('../../ test')

import requests, json, jwt
from ld4apps.rdf_json import URI, BNode, RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder
from ld4apps.base_constants import RDF, DC, AC, AC_ALL, ADMIN_USER, CE, VCARD, FOAF, ANY_USER, AC_T, AC_R, AC_C, AC_D, AC_W, AC_X
import pytest
import ld4apps.test.test_helper as test_helper
from ld4apps.test.test_helper import USER1_URL, USER2_URL, HS_HOSTNAME, ac_container_url

TENANT_TEST = 'Test Tenant'
mt_container_url = 'http://%s/mt' % HS_HOSTNAME
mt_sites_url = 'http://%s/mt/sites' % HS_HOSTNAME
mt_capabilities_url = 'http://%s/mt/capabilities' % HS_HOSTNAME


def test_basic_crud():
    # create a usergroup that gives the admin user full permissions to the root ('/') resource group
    #   this is needed because the /mt/sites uses the '/' resource group to check permissions
    body = {
        '': {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who': [
                URI(ADMIN_USER)
            ],
            AC+'may': [URI('#permission_1')],
        },
        '#permission_1': {
            AC+'do': AC_ALL,
            AC+'to': [URI('/')]
        }
    }
    test_helper.create(ac_container_url, body, ADMIN_USER)

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

#TODO: test MultiTenant functionality better

# this is for working with tests while building them
if __name__ == "__main__":
    test_basic_crud()
    pass