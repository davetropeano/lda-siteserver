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
mt_container_url = 'http://%s/mt' % HS_HOSTNAME

def test_basic_crud():
    test_helper.container_crud_test(mt_container_url, DC+'title', RDF+'test', 'test post', 'test patch')