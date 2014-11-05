import requests, json, jwt
from rdf_json import URI, BNode, RDF_JSON_Encoder, RDF_JSON_Document, rdf_json_decoder
from base_constants import RDF, DC, AC, AC_ALL, ADMIN_USER, CE, VCARD, FOAF, ANY_USER, AC_T, AC_R, AC_C, AC_D, AC_W, AC_X
import pprint
pp = pprint.PrettyPrinter(indent=4)

TEST_USER = 'http://ibm.com/ce/user/test'
HS_HOSTNAME = 'localhost:3001'
ac_container_url = 'http://%s/ac' % HS_HOSTNAME
account_container_url = 'http://%s/account' % HS_HOSTNAME

def make_headers(type='GET', user=None, password=None,modificationCount=None):
    if type not in ('GET', 'POST', 'PATCH', 'DELETE'):
        raise Exception('invalid header type')

    header = {}

    if user == ADMIN_USER:
        pass
    if user is not None:
        password = 'our little secret'
        encoded_signature = jwt.encode({'user': user}, password, 'HS256')
        header.update({'Cookie': 'SSSESSIONID=%s' % encoded_signature})

    if type == 'GET':
        header.update({'Accept': 'application/rdf+json+ce'})
    elif type == 'POST':
        header.update({'Content-type': 'application/rdf+json+ce'})
        #this is something about POST Action
        header.update({'ce-post-reason': 'ce-create'})
    elif type == 'PATCH':
        header.update({'Content-type': 'application/rdf+json+ce'})
        header.update({'CE-ModificationCount': modificationCount})

    return header

def container_crud_test(container_url, post_body, patch_prop, patch_value):
    patch_body = {
        '' : {
            patch_prop: patch_value
            }
        }

    # test post
    headers = make_headers('POST', ADMIN_USER)
    r = requests.post(container_url, headers=headers, data=json.dumps(post_body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 201
    r_doc = RDF_JSON_Document(r)
    # verify that the patch property of the posted document equals the resulting document
    assert r_doc[r_doc.default_subject()][patch_prop] == post_body[''][patch_prop]

    # patch
    headers = make_headers('PATCH', ADMIN_USER, modificationCount=0)
    r = requests.patch(r_doc.default_subject(), headers=headers, data=json.dumps(patch_body, cls=RDF_JSON_Encoder), verify=False)
    print r.text
    assert r.status_code == 200

    # test get
    body = {}
    headers = make_headers('GET', ADMIN_USER)
    r = requests.get(r_doc.default_subject(), headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 200
    r_doc = RDF_JSON_Document(r)
    # verify that the patch property has the new value
    assert r_doc[r_doc.default_subject()][patch_prop] == patch_value

    # delete
    body = {}
    headers = make_headers('DELETE', ADMIN_USER)
    r = requests.delete(r_doc.default_subject(), headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 200

    # verify that the document has been deleted
    body = {}
    headers = make_headers('GET', ADMIN_USER)
    r = requests.get(r_doc.default_subject(), headers=headers, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    assert r.status_code == 404