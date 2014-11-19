import operation_primitives
import example_logic_tier as base
import Cookie
import urlparse, urllib
import logging
import cryptography
import os, binascii
import rdf_json
import time
import utils
from rdf_json import URI
from base_constants import CE, RDF, VCARD, FOAF, ADMIN_USER
    
logging.basicConfig(level=logging.DEBUG)
MEMBER_IS_OBJECT                =   True
MEMBER_IS_SUBJECT               =   False

class Domain_Logic(base.Domain_Logic):
    def default_resource_group(self):
        if self.namespace == 'account':
            return self.document_url()
        return super(Domain_Logic, self).default_resource_group()

    def put_document(self, document):
        return(404, [], [('', 'PUT not supported')])

    def create_document(self, document):
        # we do not authenticate - new user trying to create account
        if self.tenant == 'hostingsite' and self.namespace == 'account':
            return self.create_account(document)
        else:
            return(404, [], [('', 'unknown collection %s' % self.path)])

    def execute_query(self, query):
        if self.tenant == 'hostingsite' and self.document_id == 'login':
            # login is a special kind of query on the 'account' collection. It's the only one you can do without having already logged on
            return self.process_login(query)
        else:
            return(404, [], [('', 'unknown query %s' % self.path)])

    def execute_action(self, document):
        if self.tenant == 'hostingsite' and self.document_id == 'logout':
            return (200, self.append_session_headers(None, []), [])
        else:
            super(Domain_Logic, self).execute_action()

    def get_document(self):
        if self.tenant == 'hostingsite' and self.namespace == 'account' and self.document_id == 'login':
            resource_jso = {RDF+'type': URI(CE+'Login'), CE+'registration-page': URI(urlparse.urljoin(self.request_url(), '/account/new'))}
            rdf_json_doc = rdf_json.RDF_JSON_Document({self.request_url(): resource_jso}, self.request_url())
            return (200, [], rdf_json_doc)
        elif self.tenant == 'hostingsite' and self.namespace == 'account' and self.document_id == 'new':
            resource_jso = {RDF+'type': URI(CE+'Account'), CE+'account-container': URI(urlparse.urljoin(self.request_url(), '/account'))}
            rdf_json_doc = rdf_json.RDF_JSON_Document({self.request_url(): resource_jso}, self.request_url())
            return (200, [], rdf_json_doc)
        return super(Domain_Logic, self).get_document()
            
    def process_login(self, json_document):
        document = rdf_json.RDF_JSON_Document(json_document, json_document.iterkeys().next())
        try:
            accountId = document.get_value(CE+'account_id')
            password = document.get_value(CE+'password')
        except (KeyError):
            return (400, [], [('','could not extract accountId and password')])        
        field_errors = []
        if not accountId: 
            field_errors.append([CE+'account_id', 'must not be null'])
        if not password: 
            field_errors.append([CE+'password', 'must not be null'])
        if len(field_errors) == 0:
            status, account = operation_primitives.get_document(self.user, self.request_hostname, self.tenant, 'account', accountId)
            if status == 200:
                userURL = account.get_value(CE+'user')
                salt = account.get_value(CE+'salt')
                stored_hash = cryptography.durable_decrypt(str(account.get_value(CE+'password')))
                password_hash = cryptography.hex_hash(salt + password)
                if password_hash == stored_hash:
                    return (200, self.append_session_headers(account, []), account)
                else:
                    return (404, [], [('','That accountId and password not found')])
            else:
                return (status, [], account)
        else:
            return (400, [], field_errors)

    def create_account(self, json_document):
        # Only PUT will set account_id. If account_id is None, then self.document_id refers to a collection being posted to, not the account.
        password_hash = userURL = None
        field_errors = []
        document = rdf_json.RDF_JSON_Document(json_document, '')
        try: 
            account_id = document.get_value(CE+'account_id')
            if not account_id: 
                field_errors.append([CE+'account_id', 'must provide account_id'])
            password = document.get_value(CE+'password')
            if password:
                if len(field_errors) == 0:
                    salt = binascii.b2a_hex(os.urandom(16))
                    document.set_value(CE+'salt', salt)
                    encrypted_hash = cryptography.durable_encrypt(cryptography.hex_hash(salt + password))
                    document.set_value(CE+'password', encrypted_hash)
            else: 
                field_errors.append([CE+'password', 'must not be null'])
            email = document.get_value(VCARD+'email')
            if email:
                document.set_value(VCARD+'email', cryptography.durable_encrypt(email)) # better not store email addresses in clear text
            else:
                field_errors.append([VCARD+'email', 'must not be null'])
            userURL = document.get_value(CE+'user')
            if userURL:
                if account_id:
                    userURL = normalize_url(str(userURL), 'http://%s%s/%s' % (self.request_hostname, self.path, account_id))
                    document.set_value(CE+'user', URI(userURL))
            else:
                field_errors.append([CE+'user', 'must not be null'])
        except KeyError as e :
            return (400, [], [('','KeyError %s in %s' % (e, repr(document)))])
        if account_id:
            status, body = operation_primitives.get_document(ADMIN_USER, self.request_hostname, self.tenant, self.namespace, account_id)
            if status == 200: #oops - account already exists
                field_errors.append([CE+'id', 'already exists'])
        if userURL:
            query = {'_any': { CE+'user' : userURL}} 
            status, body = operation_primitives.execute_query(ADMIN_USER, query, self.request_hostname, self.tenant, self.namespace)
            if status == 200 and len(body) > 0: # an account for this user already exists
                field_errors.append([CE+'user', 'an account for user %s already exists' % userURL])
        if len(field_errors) == 0:
            self.user = userURL
            #TODO: declare CE+'user' as a unique key in DB to close timing hole between the above check (account for user already exists) and
            #      the following create_document call.
            status_code, headers, json_document = super(Domain_Logic, self).create_document(document, account_id)
            if status_code == 201:
                self.append_session_headers(json_document, headers)
                return (201, headers, json_document)
            else:
                field_errors.append(['', "unexpected error: %s %s" % (str(status_code), str(body))])
        return (400, [], field_errors)

    def append_session_headers(self, account, headers):
        if account:
            userURL = str(account.get_value(CE+'user'))
            displayName = account.get_value(FOAF+'nick', userURL, "")
            if not displayName or displayName == "":
                displayName = account.get_value(FOAF+'givenName', userURL, "")
                if not displayName or displayName == "":
                    displayName = account.get_value(CE+'account_id')
            fkaURL = utils.get_claims(self.environ)['user']
            claims = { # normal RDF_JSON turns out to be too voluminous. Make something small
                'exp': time.time() + 3600,
                'user': userURL,
                'acc': account.graph_url, #TODO remove this
                'disp': displayName,
                'fka': fkaURL }
        else:
            claims = utils.create_anonymous_user_claims(self.environ)
        sessionId = cryptography.encode_jwt(claims) 
        cookie = Cookie.SimpleCookie()
        cookie['SSSESSIONID'] = sessionId # SSSESSIONID  is 'Site Server Session ID'
        cookie['SSSESSIONID']['path'] = '/'
        cookie['user'] = claims['user']
        cookie['user']['path'] = '/'
        cookie_headers = map(lambda morsel: ('Set-Cookie', morsel.OutputString()), cookie.values())
        headers.extend(cookie_headers)
        return headers
        
def normalize_url(url, reference_url):
    scheme, netloc, path, qs, fragment = urlparse.urlsplit(url)
    if (scheme == '' or scheme == 'http') and netloc == '': # http relative url
        abs_url = urlparse.urljoin(reference_url, url) #make it absolute first
        scheme, netloc, path, qs, fragment = urlparse.urlsplit(abs_url)
    path = urllib.quote(path)
    qs = urllib.quote(qs)
    return urlparse.urlunsplit((scheme.lower(), netloc.lower(), path, qs, fragment))
