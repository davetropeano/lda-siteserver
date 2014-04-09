import requests, sys, json
from rdf_json import URI, BNode, RDF_JSON_Encoder
from base_constants import RDF, CE, VCARD, FOAF, AC, AC_R, AC_C, ANY_USER, ADMIN_USER
from cryptography import encode_jwt

encoded_signature = encode_jwt({'user':ADMIN_USER})
CONTENT_RDF_JSON_HEADER = {
    'Content-type' : 'application/rdf+json+ce', 
    'Cookie' : 'SSSESSIONID=%s' % encoded_signature, 
    'ce-post-reason' : 'ce-create' 
    }

#DATASERVER_HOST = 'cloudapps4.me'
DATASERVER_HOST = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else 'localhost:3001'
if DATASERVER_HOST.startswith('localhost'):
    HOSTINGSITE_HOST = DATASERVER_HOST
else:
    HOSTINGSITE_HOST = 'hostingsite.' + DATASERVER_HOST

ac_container_url = 'http://%s/ac' % HOSTINGSITE_HOST
account_container_url = 'http://%s/account' % HOSTINGSITE_HOST

def run():
    requests.delete(ac_container_url, headers=CONTENT_RDF_JSON_HEADER)
    requests.delete(account_container_url, headers=CONTENT_RDF_JSON_HEADER)

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