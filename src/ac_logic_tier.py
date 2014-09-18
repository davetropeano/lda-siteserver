import example_logic_tier as base
import urllib, utils, os, jwt, cryptography
import rdf_json
from rdf_json import URI
import operation_primitives
from base_constants import AC, CE, AC_R, AC_C, AC_A, AC_ALL, ANY_USER, ADMIN_USER
from base_constants import URL_POLICY as url_policy

NAMESPACE_MAPPINGS = {AC : 'ac'}
NAMESPACE_MAPPINGS.update(base.NAMESPACE_MAPPINGS)
CHECK_ACCESS_RIGHTS = os.environ.get('CHECK_ACCESS_RIGHTS') != 'False'

class Domain_Logic(base.Domain_Logic):
    def namespace_mappings(self):
        return NAMESPACE_MAPPINGS
        
    def default_resource_group(self):
        if self.namespace == 'ac':
            return self.document_url()
        return super(Domain_Logic, self).default_resource_group()
    
    def permissions_by_subject(self, subject_uri):
        subject_uri = str(subject_uri)
        
        # if it's the null uri then return AC_ALL        
        if subject_uri == '' or self.user == ADMIN_USER:
            return 200, AC_ALL
        
        # check to see if the owner is the relevant_user (TODO: confirm this approach in code review)        
        headers = {
            'Accept': 'application/rdf+json+ce',
            'Cookie' : 'SSSESSIONID=%s' % cryptography.encode_jwt({'user': self.user})
        }
        r = utils.intra_system_get(subject_uri, headers)
        if r.status_code == 200:
            document = rdf_json.RDF_JSON_Document(r)
            owner = document.get_value(CE+'owner')
            if str(owner) == self.user:
                return 200, AC_ALL
        
        # subject isn't null and user isn't owner so now do actual permission check
        permissions_url = url_policy.construct_url(self.request_hostname, self.tenant, 'ac-permissions') + ('?%s&%s' % (urllib.quote(subject_uri), urllib.quote(self.user)))
        r = utils.intra_system_get(permissions_url)
        if r.status_code == 200:
            return 200, int(r.text)
        else:
            return r.status_code, 'url: %s text: %s' % (permissions_url, r.text)
    
    def insert_document(self, container, document, document_id=None):
        document = rdf_json.RDF_JSON_Document(document, '')
        if CHECK_ACCESS_RIGHTS:
            # get all the uris that this UserGroup is granting access rights to
            ac_mays = document.get_value(AC+'may')
            to_uris = []
            for may in ac_mays: 
                ac_may_props = document.get_properties(may)
                for to in ac_may_props[AC+'to']:
                    to_uris.append(to)
            # make sure the user has ADMIN permissions on all of them
            for to_uri in to_uris:
                status, permissions = self.permissions_by_subject(to_uri)
                if status == 200:
                    if not permissions & AC_A:
                        return 403, [], [('', 'not authorized')]
                else:
                    return 403, [], [('', 'unable to retrieve permissions. status: %s text: %s' % (status, permissions))]
        # below this is a copy of example_logi_tier.insert_document 
        # should permission check be split out form that so this code doesn't have to be copied? 
        self.complete_document_for_container_insertion(document, container)
        self.complete_document_for_storage_insertion(document)
        self.preprocess_properties_for_storage_insertion(document)
        status, location, result = operation_primitives.create_document(self.user, document, self.request_hostname, self.tenant, self.namespace, document_id)
        if status == 201:
            if self.change_tracking:
                self.generate_change_event(CREATION_EVENT, location)
            # Todo: fix up self.document_id, self.path, self.path_parts to match location url of new document
            self.complete_result_document(result)
            return status, [('Location', str(location))], result
        else:
            return status, [], [('', result)]
        
    def get_document(self):
        # in this section we are checking for URLs of the form <predicate>?<container membershipSubject or Object URL>
        user = self.user
        
        if self.document_id == None and self.namespace == 'ac-permissions': 
            query_parts = self.query_string.split('&')
            relevant_user = URI(urllib.unquote(query_parts[1]) if len(query_parts) > 1 else user)
            permitted_users = {'$or' : [{AC+'who' : relevant_user}, {AC+'who' : URI(ANY_USER)}]}
            resource_group = URI(urllib.unquote(query_parts[0]))
            query = {'_any_1': permitted_users, '_any_2': {AC+'to' : resource_group}}
            status, result = operation_primitives.execute_query(user, query, self.request_hostname, self.tenant, 'ac')
            answer = 0
            if status == 200:
                for rdf_json_document in result:
                    permissions = rdf_json_document.get_values(AC+'may')
                    for permission in permissions:
                        permission_to = rdf_json_document.get_values(AC+'to', str(permission))
                        if resource_group in permission_to:
                            answer = answer | rdf_json_document.get_value(AC+'do', str(permission))
            return (status, [], answer)
        elif self.document_id == None and self.namespace == 'ac-resource-groups':
            relevant_user = URI(urllib.unquote(self.query_string) if len(self.query_string) > 0 else user)
            permitted_users = {'$or' : [{AC+'who' : relevant_user}, {AC+'who' : URI(ANY_USER)}]}
            query = {'_any_1': permitted_users}
            status, result = operation_primitives.execute_query(user, query, self.request_hostname, self.tenant, 'ac')
            answer = set()
            if status == 200:            
                for rdf_json_document in result:
                    permissions = rdf_json_document.get_values(AC+'may')
                    for permission in permissions:
                        permission_to = rdf_json_document.get_values(AC+'to', str(permission))
                        permission_do = rdf_json_document.get_value(AC+'do', str(permission))
                        if permission_do | AC_R: #gives permission to read
                            answer.update(permission_to)
            return (status, [], list(answer))
        elif self.document_id == None and self.namespace == 'ac':
            if self.query_string and self.query_string != 'non-member-properties':
                query_parts = self.query_string.split('&')
                relevant_user = URI(urllib.unquote(query_parts[1]) if len(query_parts) > 1 and query_parts[1] else user)
                permitted_users = {'$or' : [{AC+'who' : relevant_user}, {AC+'who' : URI(ANY_USER)}]}
                resource_group = URI(urllib.unquote(query_parts[0]))
                if resource_group:
                    query = {'_any_1': permitted_users, '_any_2': {AC+'to' : resource_group}}
                else:
                    query = {'_any_1': permitted_users}
                status, result = operation_primitives.execute_query(user, query, self.request_hostname, self.tenant, self.namespace)
                answer = set()
                if status == 200:            
                    for rdf_json_document in result:
                        answer.add(rdf_json_document.graph_url)
                return (status, [], list(answer))

        return super(Domain_Logic, self).get_document()