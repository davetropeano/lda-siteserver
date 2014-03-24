import example_logic_tier as base
import urllib
import operation_primitives
from rdf_json import URI
from base_constants import AC, AC_R, ANY_USER

NAMESPACE_MAPPINGS = {AC : 'ac'}
NAMESPACE_MAPPINGS.update(base.NAMESPACE_MAPPINGS)

class Domain_Logic(base.Domain_Logic):
    def namespace_mappings(self):
        return NAMESPACE_MAPPINGS
        
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
                    permissions = rdf_json_document.getValues(AC+'may')
                    for permission in permissions:
                        permission_to = rdf_json_document.getValues(AC+'to', None, str(permission))
                        if resource_group in permission_to:
                            answer = answer | rdf_json_document.getValue(AC+'do', None, str(permission))
            return (status, [], answer)
        elif self.document_id == None and self.namespace == 'ac-resource-groups':
            relevant_user = URI(urllib.unquote(self.query_string) if len(self.query_string) > 0 else user)
            permitted_users = {'$or' : [{AC+'who' : relevant_user}, {AC+'who' : URI(ANY_USER)}]}
            query = {'_any_1': permitted_users}
            status, result = operation_primitives.execute_query(user, query, self.request_hostname, self.tenant, 'ac')
            answer = set()
            if status == 200:            
                for rdf_json_document in result:
                    permissions = rdf_json_document.getValues(AC+'may')
                    for permission in permissions:
                        permission_to = rdf_json_document.getValues(AC+'to', None, str(permission))
                        permission_do = rdf_json_document.getValue(AC+'do', None, str(permission))
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