import sys
sys.path.append('../../../lda-serverlib')
sys.path.append('../../../lda-serverlib/logiclibrary')
sys.path.append('../../../lda-serverlib/mongodbstorage')
sys.path.append('../../../lda-clientlib/python')
sys.path.append('../../../lda-clientlib/python/test')
sys.path.append('../../src')
sys.path.append('../../ test')

import requests, json
from ld4apps.rdf_json import URI, BNode, RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder
from ld4apps.base_constants import RDF, DC, AC, AC_ALL, ADMIN_USER, CE, VCARD, FOAF, ANY_USER, AC_T, AC_R, AC_C, AC_D, AC_W, AC_X
import ld4apps.test.test_helper as test_helper
from ld4apps.test.test_helper import USER1_URL, USER2_URL, HS_HOSTNAME, account_container_url, ac_container_url


def basic_crud(user):
    post_body = {
        '': {
            RDF+'type': URI(AC+'UserGroup'),
            DC+'title': 'test usergroup',
            AC+'who': [
                URI(ANY_USER)
            ],
            AC+'may': [
                URI('#permission_1'),
                URI('#permission_2')
            ]
        },
        '#permission_1': {
            AC+'do': AC_R,
            AC+'to': [URI('/')]
        },
        '#permission_2': {
            AC+'do': AC_C,
            AC+'to': [URI('/account'), URI('/mt/sites')]
        }
    }
    patch_prop = DC+'title'
    patch_val = 'updated test usergroup'
    test_helper.container_crud_test(ac_container_url, post_body, patch_prop, patch_val, user)


def test_basic_crud_as_anon():
    pass
    #basic_crud(None)


def test_basic_crud_as_admin():
    basic_crud(ADMIN_USER)


def test_basic_crud_as_user():
    basic_crud(USER1_URL)


def admin_create_account_usergroup():
    # give everyone access to create new accounts
    body = {
        '': {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who': [
                URI(ANY_USER)
            ],
            AC+'may': [URI('#permission_1')],
        },
        '#permission_1': {
            AC+'do': AC_C,
            AC+'to': [URI(account_container_url)]
        }
    }
    #body = {}
    headers = test_helper.make_headers('POST', ADMIN_USER)
    r = requests.post(ac_container_url, headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    return r


# this is for working with tests while building them
if __name__ == "__main__":
    test_basic_crud_as_admin()
    pass