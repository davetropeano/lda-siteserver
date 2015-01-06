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

USER1_URL = '%s/test1#owner' % account_container_url
USER2_URL = '%s/test2#owner' % account_container_url


def test_basic_crud(account_user1):
    """
    :param account_user1: this is automatically passed in by py.test.  It is the result of creating test1 account.
    """

    # CRUD test on account has to be done a little different since we switch security contexts after create
    resource_url = account_user1.default_subject()

    # this tests both read and update
    test_helper.update(resource_url, patch_prop=DC+'title', patch_value='my title', username=USER1_URL)

    # should we be able to delete an account?


def test_anon_access_to_test1_account(account_user1):
    """
    :param account_test1: RDF_Document passed in via py.test
    verify that anonymous users can't access test1 account
    """
    resource_url = account_user1.default_subject()
    test_helper.resource_access_test(
        resource_url, username=None, patch_prop=DC+'title', patch_value='anon update',
        assert_code_read=401, assert_code_update=401, assert_code_delete=401)


def test_admin_access_to_test1_account(account_user1):
    """
    :param account_user1: RDF_Document passed in via py.test
    verify that admin user can't access test1 account
    """
    resource_url = account_user1.default_subject()
    test_helper.resource_access_test(
        resource_url, username=ADMIN_USER, patch_prop=DC+'title', patch_value='admin update',
        assert_code_read=401, assert_code_update=401, assert_code_delete=401)


def test_user2_access_to_test1_account(account_user1, account_user2):
    """
    :param account_user1: RDF_Document passed in via py.test
    :param account_user2: RDF_Document passed in via py.test
    verify that one user can't access another users account
    """
    resource_url = account_user1.default_subject()
    test_helper.resource_access_test(
        resource_url, username=USER2_URL, patch_prop=DC+'title', patch_value='user2 update',
        assert_code_read=401, assert_code_update=401, assert_code_delete=401)

    resource_url = account_user2.default_subject()
    test_helper.resource_access_test(
        resource_url, username=USER1_URL, patch_prop=DC+'title', patch_value='user1 update',
        assert_code_read=401, assert_code_update=401, assert_code_delete=401)


@pytest.fixture(scope="session")
def account_user1():
    body = {
        '': {
            RDF+'type': URI(CE+'Account'),
            CE+'account_id': 'test1',
            CE+'password': 'test1',
            VCARD+'email': 'test1@us.ibm.com',
            CE+'user': URI('#owner'),
            VCARD+'adr': BNode('_:address'),
            DC+'title': 'test1 account',
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
            CE+'account_id': 'test2',
            CE+'password': 'test2',
            VCARD+'email': 'test2@us.ibm.com',
            CE+'user': URI('#owner'),
            VCARD+'adr': BNode('_:address'),
            DC+'title': 'test2 account',
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

# this is for working with tests while building them
if __name__ == "__main__":
    #r_doc = test_helper.read('http://hostingsite.localhost:3001/account/test1', username='test1')

    user1_r_doc = account_user1()
    user2_r_doc = account_user2()
    test_anon_access_to_test1_account(user1_r_doc)
    pass