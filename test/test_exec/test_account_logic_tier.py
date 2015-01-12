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
    :param account_user1: RDF_Document passed in via py.test
    verify that anonymous users can't access user1 account
    """
    resource_url = account_user1.default_subject()
    test_helper.resource_access_test(
        resource_url, username=None, patch_prop=DC+'title', patch_value='anon update',
        assert_code_read=401, assert_code_update=401, assert_code_delete=401)


def test_admin_access_to_test1_account(account_user1):
    """
    :param account_user1: RDF_Document passed in via py.test
    verify that admin user can't access user1 account
    """
    resource_url = account_user1.default_subject()
    test_helper.resource_access_test(
        resource_url, username=ADMIN_USER, patch_prop=DC+'title', patch_value='admin update',
        assert_code_read=401, assert_code_update=401, assert_code_delete=401)


def test_user2_access_to_test1_account(account_user1, account_user2):
    """
    :param account_user1: RDF_Document passed in via py.test
    :param account_user2: RDF_Document passed in via py.test
    verify that one user can't access another user's account
    """
    resource_url = account_user1.default_subject()
    test_helper.resource_access_test(
        resource_url, username=USER2_URL, patch_prop=DC+'title', patch_value='user2 update',
        assert_code_read=401, assert_code_update=401, assert_code_delete=401)

    resource_url = account_user2.default_subject()
    test_helper.resource_access_test(
        resource_url, username=USER1_URL, patch_prop=DC+'title', patch_value='user1 update',
        assert_code_read=401, assert_code_update=401, assert_code_delete=401)


# this is for working with tests while building them
if __name__ == "__main__":
    #user1_rdoc = account_user1()
    #user2_rdoc = account_user2()
    #test_user2_access_to_test1_account(user1_rdoc, user2_rdoc)
    pass