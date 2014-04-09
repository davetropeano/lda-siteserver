import base64, requests, sys
import json
from rdf_json import URI, BNode, RDF_JSON_Encoder
from base_constants import ADMIN_USER
from cryptography import encode_jwt

encoded_signature = encode_jwt({'user':ADMIN_USER})
CONTENT_RDF_JSON_HEADER = {
    'Content-type' : 'application/rdf+json+ce', 
    'Cookie' : 'SSSESSIONID=%s' % encoded_signature, 
    'ce-post-reason' : 'ce-create' 
    }

#DATASERVER_HOSTNAME = 'cloudapps4.me'
DATASERVER_HOSTNAME = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else 'localhost:3001'

XSD = 'http://www.w3.org/2001/XMLSchema#'
RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
DC = 'http://purl.org/dc/terms/'
CE = 'http://ibm.com/ce/ns#'
VCARD = 'http://www.w3.org/2006/vcard/ns#'
FOAF = 'http://xmlns.com/foaf/0.1/'

account_container_url = 'http://%s/account' % DATASERVER_HOSTNAME

def run():
    requests.delete(account_container_url, headers=CONTENT_RDF_JSON_HEADER)

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