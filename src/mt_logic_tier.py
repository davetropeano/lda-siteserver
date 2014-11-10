import operation_primitives
import example_logic_tier as base
import rdf_json 
from rdf_json import URI
import logging    
import utils
import os, urlparse
from base_constants import CE, AC, RDF, AC_ALL, LDP, ADMIN_USER
from base_constants import URL_POLICY as url_policy
logging.basicConfig(level=logging.DEBUG)

MEMBER_IS_OBJECT                =   True
MEMBER_IS_SUBJECT               =   False

class Domain_Logic(base.Domain_Logic):
    def default_resource_group(self):
        if self.namespace == 'mt' and self.document_id == 'sites':
            return self.document_url()
        return super(Domain_Logic, self).default_resource_group()

    def create_document(self, document):
        if self.user is None:
            return (401, [], None)
        else:
            if self.tenant == 'hostingsite' and self.namespace == 'mt' and self.document_id == 'sites':
                return self.create_site(document)
            elif self.tenant == 'hostingsite' and self.namespace == 'mt' and self.document_id == 'capabilities':
                rdf_doc = rdf_json.RDF_JSON_Document(document, '')
                if str(rdf_doc.get_value(RDF+'type')) == CE+'Capability':
                    return self.create_capability(document)
            elif self.tenant == 'hostingsite' and self.namespace == 'mt' and self.document_id != 'none' and self.extra_path_segments and self.extra_path_segments[0] == 'properties':
                return super(Domain_Logic, self).create_document(document)
            return(404, [], [('', 'unknown collection %s' % self.path)])

    def put_document(self, document):
        return(404, [], [('', 'PUT not supported')])

    def execute_query(self, query):
        return(400, [], [('', 'unknown query %s' % self.path)])

    def get_document(self):
        if self.tenant == 'hostingsite' and self.path == '/' : #home page
            resource_url = url_policy.construct_url(self.request_hostname, self.tenant)
            rdf_json_doc = rdf_json.RDF_JSON_Document({
                resource_url: {
                    RDF+'type': URI(CE+'Saas_host'),
                    #CE+'sites': URI(url_policy.construct_url(None, 'hostingsite', 'mt', 'sites'))
                    CE+'sites': URI(url_policy.construct_url(None, None, 'mt', 'sites'))
                    }
                }, resource_url)
            return (200, [], rdf_json_doc)   
        elif self.path == '/': # home page for a particular tenant
            if self.user is None:
                return (401, [], None)
            else:
                status, document = operation_primitives.get_document(self.user, self.request_hostname, 'hostingsite', 'mt', self.tenant)
                if status == 200:
                    site_home = document.get_value(CE+'site_home').uri_string
                    return [301, [('Location', str(site_home))], None]
                return [status, [], document]
        elif self.tenant == 'hostingsite' and self.namespace == 'mt' and self.document_id == 'sites': #bpc container of all sites visible to the user
            if self.user is None and self.extra_path_segments and len(self.extra_path_segments) == 1 and self.extra_path_segments[0] == 'new':
                return (401, [], None)
            member_resource = url_policy.construct_url(self.request_hostname)
            container_url = url_policy.construct_url(self.request_hostname, self.tenant, 'mt', 'sites')
            document = self.create_container(container_url, member_resource, CE+'sites', MEMBER_IS_OBJECT)
            status, document = self.complete_request_document(document)
            return (status, [], document)
        elif self.namespace == 'mt' and self.document_id == 'capabilities': #bpc container of all capabilities visible to the user
            member_resource = url_policy.construct_url(self.request_hostname)
            container_url = url_policy.construct_url(self.request_hostname, self.tenant, 'mt', 'capabilities')
            document = self.create_container(container_url, member_resource, CE+'capabilities', MEMBER_IS_OBJECT)
            status, document = self.complete_request_document(document)
            return (status, [], document)
        return super(Domain_Logic, self).get_document()

    def add_bpc_member_properties(self, container, query=None):
        if str(container.get_value(LDP+'membershipResource')) == url_policy.construct_url(self.request_hostname) and str(container.get_value(LDP+'hasMemberRelation')) == CE+'capabilities':
            try:
                #tricky code - change tenant to cause the query to look for data in the hostingsite's collections, not the requestor's (tenant's)
                #since all stored data is relative to an implicit host (domain), this will find the same data for each tenant domain. 
                #Each resource that is found will be returned in the tenants domain, so capabilities are automatically mirrored in all tenant domains
                #although they are only really stored in the hostingsite domain's collections
                original_tenant = self.tenant
                self.tenant = 'hostingsite' 
                result = super(Domain_Logic, self).add_bpc_member_properties(container, query)
            finally:
                self.tenant = original_tenant 
            return result
        else:
            return super(Domain_Logic, self).add_bpc_member_properties(container, query)
        
    def complete_result_document(self, document):
        # in this section we add any calculated triples
        document_url = document.graph_url    
        types = document.get_values(RDF+'type')
        if URI(CE+'Site') in types:
            improvements = document.get_values(CE+'improvements')
            tenant_id = self.document_id
            tenant_base_url = url_policy.construct_url(self.request_hostname, tenant_id)
            if len(improvements) > 0: # turn these relative URLs to absolute
                abs_improvement_urls = [urlparse.urljoin(tenant_base_url, rel_improvement_url) for rel_improvement_url in improvements]
                document.set_value(CE+'improvements', abs_improvement_urls)
            document.add_triples(document_url, CE+'site_capabilities', url_policy.construct_url(self.request_hostname, tenant_id, 'mt', 'capabilities'))
        return super(Domain_Logic, self).complete_result_document(document)

    def patch_document(self, request_body):
        if self.tenant == 'hostingsite' and self.namespace == 'mt' and self.document_id != None:
            return super(Domain_Logic, self).patch_document(request_body)
        else:
            return (400, [], [('','Patch Not yet implemented')])

    def preprocess_properties_for_storage_insertion(self, rdf_json):
        def make_relative(improvement_url):
            abs_url_str = urlparse.urljoin(self.request_url(), str(improvement_url))
            parsed_url = []
            parsed_url.extend(urlparse.urlparse(abs_url_str))
            parsed_url[0] = '' 
            parsed_url[1] = ''
            return urlparse.urlunparse(parsed_url)
        improvements = rdf_json.get_values(CE+'improvements')
        if len(improvements) > 0: # turn these absolute URLs to relative
            rdf_json.set_value(CE+'improvements', [make_relative(improvement_url) for improvement_url in improvements])
            
    def create_site(self, document):
        if self.user is None:
            return (401, [], None)
        field_errors = []
        site = rdf_json.RDF_JSON_Document(document, '')
        site_types = site.get_values(RDF+'type')
        if URI(CE+'Site') not in site_types: 
            field_errors.append(['', 'site must have a type of CE Site'])
        site_id = site.get_value(CE+'site_id')
        if not (site_id):
            field_errors.append(['', 'must set CE+"site_id" for site'])
        else:
            if not site_id.isalpha():
                field_errors.append(['', 'site id must be alphanumeric'])
            else:
                if not site_id.islower():
                    field_errors.append(['', 'site id must be lowercase'])                
        if len(field_errors) == 0:
            status, body = operation_primitives.get_document(ADMIN_USER, self.request_hostname, 'hostingsite', 'mt', site_id) 
            if status == 200 or site_id == 'sites': #oops - site already exists
                field_errors.append([CE+'id', 'site already exists'])
            else:
                site.set_value(AC+'resource-group', URI('')) #group for a site is itself
                status, headers, body = super(Domain_Logic, self).create_document(site, site_id)
                if status == 201:
                    # create a UserGroup that gives the current user AC_ALL permissions for the new site
                    data = {
                        '' : {
                            RDF+'type': URI(AC+'UserGroup'),
                            AC+'who' : [ URI(self.user) ],
                            AC+'may' : [ URI('#permission_1') ]
                            },
                        '#permission_1' : {
                            AC+'do' : AC_ALL,
                            AC+'to' : [ URI('/') ]
                            }
                        }
                    ac_url = url_policy.construct_url(self.request_hostname, site_id, 'ac')
                    r = utils.intra_system_post(ac_url, data)
                    if r.status_code == 201:
                        return (201, headers, body)
                    field_errors.append(['', "failed to create UserGroup: %s %s" % (str(r.status_code), r.text)])
                else:
                    field_errors.append(['', "unexpected error creating site: %s %s" % (str(status), str(body))])
        return (400, [], field_errors)

    def create_capability(self, document):
        if self.user is None:
            return (401, [], None)
        field_errors = []
        capability = rdf_json.RDF_JSON_Document(document, '')
        types = capability.get_values(RDF+'type')
        if URI(CE+'Capability') not in types: 
            field_errors.append(['', 'capability must have a type of CE Capability'])
        container = capability.get_value(CE+'improvement_container')
        if not container:
            field_errors.append([CE+'improvement_container', 'must be set'])
        improvement_type = capability.get_value(CE+'improvement_type')
        if not improvement_type:
            field_errors.append([CE+'improvement_type', 'must be set'])
        if len(field_errors) == 0:
            status_code, headers, json_document = super(Domain_Logic, self).create_document(document)
            if status_code == 201:
                return (201, headers, json_document)
            else:
                field_errors.append(['', "unexpected error creating capability: %s %s" % (str(status_code), str(json_document))])
        return (400, [], field_errors)
