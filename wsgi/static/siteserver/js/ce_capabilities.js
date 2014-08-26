"use strict";
window.siteserver = window.siteserver || {};

siteserver.CapabilitiesViewModel = function () {
    var self = this;
    self.jso = null;
    self.parentVM = null;
    self.site_model = null;
    self.capabilities = [];    
    ko.track(self);    
    self.visible = ko.observable(false);
    
    self.init = function (jso) {
        self.jso = jso;  
        self.parentVM = jso.parent;
        self.site_model = self.jso.parent.model;
        self.capabilities = self.jso.ldp_contains ? self.jso.ldp_contains : [];        
    }
    
    self.select_capability = function(data){
        var new_improvement_model = {
            _subject: "",
            rdf_type: data.ce_improvement_type,
            dc_title: data.dc_title,
            ce_capability: rdf_util.URI(data._subject)
        };
        
        var post_url = '/cat'; //TODO: is there somewhere we can look this up?
        var ss_session_id = misc_util.getSSSessionId()
        ld_util.send_create(post_url,new_improvement_model,function(request){
            if(request.status === 201) {
                var improvement_model = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
                self.parentVM.add_improvement(improvement_model);
            }
            else {
                siteserver.displayResponse(request,'error');
            }
        }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null) // going cross-origin. Pass SSSESSIONID header to avoid login challenge
    }
    
    self.navigate_back_to_site = function(){
        ViewManager.switchView(self.site_model);
    }
}
