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
from test_helper import USER1_URL, USER2_URL, account_container_url
import pytest


@pytest.fixture(scope="session")
def account_user1():
    body = {
        '': {
            RDF+'type': URI(CE+'Account'),
            CE+'account_id': 'user1',
            CE+'password': 'user1',
            VCARD+'email': 'user1@us.ibm.com',
            CE+'user': URI('#owner'),
            VCARD+'adr': BNode('_:address'),
            DC+'title': 'user1 account',
            AC+'resource-group': URI('')  # have this account be it's own resource group (default is /account)
        },
        '#owner': {
            RDF+'type': URI(FOAF+'Person'),
            FOAF+'givenName': 'FName',
            FOAF+'familyName': 'LName',
            FOAF+'nick': 'NName'
        },
        '_:address': {
            RDF+'type': URI(VCARD+'Work'),
            VCARD+'street-address': 'unknown',
            VCARD+'locality': 'Seville',
            VCARD+'region': 'Andalusia',
            VCARD+'postal-code': '00000',
            VCARD+'country-name': 'Spain'
        }
    }
    user1_r_doc = test_helper.create(container_url=account_container_url, post_body=body)
    return user1_r_doc


@pytest.fixture(scope="session")
def account_user2():
    body = {
        '': {
            RDF+'type': URI(CE+'Account'),
            CE+'account_id': 'user2',
            CE+'password': 'user2',
            VCARD+'email': 'user2@us.ibm.com',
            CE+'user': URI('#owner'),
            VCARD+'adr': BNode('_:address'),
            DC+'title': 'user2 account',
            AC+'resource-group': URI('')  # have this account be it's own resource group (default is /account)
        },
        '#owner': {
            RDF+'type': URI(FOAF+'Person'),
            FOAF+'givenName': 'FName',
            FOAF+'familyName': 'LName',
            FOAF+'nick': 'NName'
        },
        '_:address': {
            RDF+'type': URI(VCARD+'Work'),
            VCARD+'street-address': 'unknown',
            VCARD+'locality': 'Seville',
            VCARD+'region': 'Andalusia',
            VCARD+'postal-code': '00000',
            VCARD+'country-name': 'Spain'
        }
    }
    user2_r_doc = test_helper.create(container_url=account_container_url, post_body=body)
    return user2_r_doc