"use strict";
window.siteserver = window.siteserver || {};

siteserver.SiteViewModel = function () {
    var self = this;
    self.model = null;
    self.new_improvement_model = null;
    self.capabilities = [];
    self.improvements = [];
    self.error = null;    
    self.editing_site = false;
    ko.track(self);    
    self.visible = ko.observable(false);

    self.init = function (jso) {
        self.model = jso;
        if(!self.model.improvements){
            self.model.improvements = [];
        }        
        self.get_capabilities();
        self.get_improvements();
    }
    
    self.clearError = function () {
        self.error = null;
    }
    
    self.get_capabilities = function () {
        var ss_session_id = misc_util.getSSSessionId()
        ld_util.get(self.model.ce_site_capabilities, function(request){
            if (request.status==200) {
                var capabilities_jso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
                if (capabilities_jso.ldp_contains) {
                    self.capabilities = capabilities_jso.ldp_contains;
                }
            }
            else {
                console.log( request.status )
            }
        }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null) // going cross-origin. Pass SSSESSIONID header to avoid login challenge        
    }
    
    self.get_improvements = function () {
        var improvement_urls = self.model.ce_improvements;
        if (improvement_urls) {
            var ss_session_id = misc_util.getSSSessionId()
            for (var i = 0; i<improvement_urls.length; i++) {
                var improvement_url = improvement_urls[i] //calculate the tenant's domain
                ld_util.get(improvement_url, function(request) {
                    if (request.status==200) {
                        var improvement = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                        self.improvements.push(improvement)
                        self.improvements.sort(function(a,b){
                            return (b.dc_created > a.dc_created) ? -1 : (b.dc_created < a.dc_created) ? 1 : 0
                        })
                    }
                    else {
                        console.log( request.status )
                    }
                }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null) // going cross-origin. Pass SSSESSIONID header to avoid login challenge
            }
        }        
    }

    self.create_new_improvement = function () {
        self.new_improvement_model = {
            _subject: "",
            rdf_type: new rdf_util.URI(CE+'Site'),
            ce_improvement_id: "",
            dc_title: ""                
        }; 
    }
    
    self.save_new_improvement = function () {
        ld_util.send_create(self.model._subject,self.new_improvement_model,function(request){
            if(request.status === 201) {
                var improvement_model = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
                self.model.ldp_contains.push(improvement_model);
                self.model = self.model; //triggers UI to be rebuilt
                self.new_improvement_model = null;
            }
            else {
                var errors = rdf_util.parse_rdf_json(request);
                self.error = errors[0][1];
                console.log(errors);
                console.log(request); 
            }
        });
        
    }
    
    self.cancel_new_improvement = function () {
        self.new_improvement_model = null;
    }
    
    self.enter_site_edit = function(){
        self.editing_site = true;
    }
    
    self.leave_site_edit = function(){
        self.editing_site = false;
    }
    
    self.submit_site_edit = function() {
        var patch = {
                _subject: self.model._subject,
                dc_title: self.model.dc_title
        };
        var rdf_jso = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(patch)
        ld_util.send_patch(self.model._subject, self.model.ce_modificationCount, rdf_jso, function(http) {
            if (http.status==200) {
                self.model.ce_modificationCount += 1; //TODO: this could break, should do a get to get the new modification count
            }
            else{
                self.error(http.responseText) //todo - parse this out nicely
            }
            self.leave_site_edit();
        });
    }
}
