import requests, sys, json
from rdf_json import URI, BNode, RDF_JSON_Encoder
from base_constants import RDF, CE, VCARD, FOAF, AC, AC_R, AC_C, ANY_USER, ADMIN_USER
from test_utils import POST_HEADERS as CONTENT_RDF_JSON_HEADER
import test_utils

#DATASERVER_HOSTNAME = 'cloudapps4.me'
DATASERVER_HOSTNAME = 'localhost:3001'
if len(sys.argv) > 1:
    DATASERVER_HOSTNAME = sys.argv[1]
    
if DATASERVER_HOSTNAME.startswith('localhost'):
    HS_HOSTNAME = DATASERVER_HOSTNAME
else:
    HS_HOSTNAME = 'hostingsite.' + DATASERVER_HOSTNAME

ac_container_url = 'http://%s/ac' % HS_HOSTNAME
account_container_url = 'http://%s/account' % HS_HOSTNAME
mt_sites_container_url = 'http://%s/mt/sites' % HS_HOSTNAME

def run():
    #test_utils.delete(mt_sites_container_url)
    requests.delete(ac_container_url, headers=CONTENT_RDF_JSON_HEADER)
    requests.delete(account_container_url, headers=CONTENT_RDF_JSON_HEADER)
    
    # give everyone access to read from '/'
    # give everyone access to create accounts and sites
    body = {
        '' : {
            RDF+'type': URI(AC+'UserGroup'),
            AC+'who' : [
                URI(ANY_USER)
                ],
            AC+'may' : [
                URI('#permission_1'),
                URI('#permission_2')
                ]
            },
        '#permission_1' : {
            AC+'do' : AC_R,
            AC+'to' : [ URI('/') ]
            },
        '#permission_2' : {
            AC+'do' : AC_C,
            AC+'to' : [ URI('/account'), URI('/mt/sites') ]
            }
        }
    r = requests.post(ac_container_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE user group! ' + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)

    body = { \
        '' : {
            RDF+'type': URI(CE+'Account'),
            CE+'account_id' : 'explorer',
            CE+'password': 'cloud',
            VCARD+'email': 'explorer@us.ibm.com',
            CE+'user': URI('#owner'),
            VCARD+'adr' : BNode('_:address')
            },
        '#owner' : {
            RDF+'type': URI(FOAF+'Person'),
            FOAF+'givenName' : 'Juan Rodriguez',
            FOAF+'familyName' : 'Cabrillo',
            FOAF+'nick' : 'Johnny'
            },
        '_:address' : {
            RDF+'type': URI(VCARD+'Work'),
            VCARD+'street-address' : 'unknown',
            VCARD+'locality' : 'Seville',
            VCARD+'region' : 'Andalusia',
            VCARD+'postal-code' : '00000',
            VCARD+'country-name' : 'Spain'
            }
        }
    r = requests.post(account_container_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE Account! %s' % (account_container_url + '/explorer : ') + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)

    body = { \
        '' : {
            RDF+'type': URI(CE+'Account'),
            CE+'account_id' : 'admin',
            CE+'password': 'admin',
            VCARD+'email': 'admin@us.ibm.com',
            CE+'user': URI(ADMIN_USER),
            VCARD+'adr' : BNode('_:address')
            },
        ADMIN_USER : {
            RDF+'type': URI(FOAF+'Person'),
            FOAF+'givenName' : 'John',
            FOAF+'familyName' : 'Smith',
            FOAF+'nick' : 'Admin'
            },
        '_:address' : {
            RDF+'type': URI(VCARD+'Work'),
            VCARD+'street-address' : 'unknown',
            VCARD+'locality' : 'Seville',
            VCARD+'region' : 'Andalusia',
            VCARD+'postal-code' : '00000',
            VCARD+'country-name' : 'Spain'
            }
        }
    r = requests.post(account_container_url, headers=CONTENT_RDF_JSON_HEADER, data=json.dumps(body, cls=RDF_JSON_Encoder), verify=False)
    if r.status_code != 201:
        print '######## FAILED TO CREATE Account! %s' % (account_container_url + '/admin : ') + r.text
        return
    print '######## POSTed resource: %s, status: %d' % (r.headers['location'], r.status_code)
        
if __name__ == '__main__':
    run()