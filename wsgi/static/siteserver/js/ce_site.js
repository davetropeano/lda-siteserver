"use strict";
window.siteserver = window.siteserver || {};

siteserver.SiteViewModel = function () {
    var self = this;
    self.model = null;
    self.improvements = [];
    self.editing_site = false;
    ko.track(self);    
    self.visible = ko.observable(false);

    self.init = function (jso) {
        self.model = jso;
        self.get_improvements();
    }
    
    self.get_improvements = function () {
        self.improvements = [];
        var improvement_urls = self.model.ce_improvements;
        if (improvement_urls) {
            var ss_session_id = misc_util.getSSSessionId()
            for (var i = 0; i<improvement_urls.length; i++) {
                var improvement_url = improvement_urls[i] //calculate the tenant's domain
                ld_util.get(improvement_url, function(request) {
                    if (request.status==200) {
                        var improvement = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                        improvement.url = request.resource_url // can't use _subject because it;s relative to a different domain
                        self.improvements.push(improvement)
                        self.improvements.sort(function(a,b){
                            return (b.dc_created > a.dc_created) ? -1 : (b.dc_created < a.dc_created) ? 1 : 0
                        })
                    }
                    else {
                        siteserver.displayResponse(request,'error');
                    }
                }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null) // going cross-origin. Pass SSSESSIONID header to avoid login challenge
            }
        }
    }

    self.navigate_to_capabilities = function () {
        var ss_session_id = misc_util.getSSSessionId()
        ld_util.get(self.model.ce_site_capabilities, function(request){
            if (request.status==200) {
                var capabilities_jso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
                capabilities_jso.parent = self;
                ViewManager.switchView(capabilities_jso);
            }
            else {
                siteserver.displayResponse(request, 'error');
            }
        }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null) // going cross-origin. Pass SSSESSIONID header to avoid login challenge         
    }
    
    self.add_improvement = function(improvement_model){
        self.model.ce_improvements.push(improvement_model._subject);
        var patch = {
            "" : {ce_improvements : self.model.ce_improvements}
        }
        ld_util.send_patch(self.model._subject, self.model.ce_modificationCount,patch,function(response){
            if (response.status==200) {
                var patched_model = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(response);
                ViewManager.switchView(patched_model);
            }
            else {
                siteserver.displayResponse(request, 'error');
            }
        });
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
        ld_util.send_patch(self.model._subject, self.model.ce_modificationCount, rdf_jso, function(response) {
            if (response.status==200) {
                var patched_model = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(response);
                self.model = patched_model;
                self.leave_site_edit();
            }
            else{
                siteserver.displayResponse(response,'error');                
            }
        });
    }
}
