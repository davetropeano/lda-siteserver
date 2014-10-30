import example_logic_tier as base
import urllib, utils, os, jwt, cryptography
import rdf_json
from rdf_json import URI
import operation_primitives
from base_constants import AC, CE, AC_R, AC_C, AC_A, AC_ALL, ANY_USER, ADMIN_USER, RDF
from base_constants import URL_POLICY as url_policy
import logging
import requests

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
    
    def permissions_for_resource(self, resource_uri):
        resource_uri = str(resource_uri)
        resource_uri = self.absolute_url(resource_uri)
        
        # if it's the null uri then return AC_ALL        
        if resource_uri == self.request_url() or self.user == ADMIN_USER: 
            return 200, AC_ALL

        r = utils.intra_system_get(resource_uri)
        if r.status_code == 200:
            document = rdf_json.RDF_JSON_Document(r)
            owner = document.get_value(CE+'owner')
            if str(owner) == self.user:
                return 200, AC_ALL
        
        # resource_uri isn't null and user isn't owner so now do actual permission check
        permissions_url = url_policy.construct_url(self.request_hostname, self.tenant, 'ac-permissions') + ('?%s&%s' % (urllib.quote(resource_uri), urllib.quote(self.user)))
        r = utils.intra_system_get(permissions_url)
        if r.status_code == 200:
            return 200, int(r.text)
        else:
            return r.status_code, 'url: %s text: %s' % (permissions_url, r.text)
    
    def permissions(self, document, insert_document=None):
        user_group = insert_document if insert_document else document
        if type(user_group) is dict:
            user_group = rdf_json.RDF_JSON_Document(user_group, '')
        if str(user_group.get_value(RDF+'type')) == AC+'UserGroup':
            ac_mays = user_group.get_value(AC+'may')
            for may in ac_mays:
                ac_may_props = user_group.get_properties(may)
                for to in ac_may_props[AC+'to']:
                    # make sure the user has ADMIN permissions on all of them
                    status, permissions = self.permissions_for_resource(to)
                    if status == 200:
                        if not permissions & AC_A:
                            return 403, 0
                    else:
                        return status, 0
        return super(Domain_Logic, self).permissions(document, insert_document)

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