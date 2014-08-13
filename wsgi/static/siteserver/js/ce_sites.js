"use strict";
window.siteserver = window.siteserver || {};

siteserver.SitesViewModel = function () {
    var self = this;
    self.model = null;
    self.new_site_model = null;
    self.error = null;

    ko.track(self);

    self.visible = ko.observable(false);

    self.init = function (jso) {
        self.model = jso;
        if (!self.model.ldp_contains) {
            self.model.ldp_contains = [];
        }        
    }
    
    self.clear_error = function () {
        self.error = null;
    }
    
    self.new_site = function () {
        self.new_site_model = {
            _subject: "",
            rdf_type: new rdf_util.URI(CE+'Site'),
            ce_site_id: "",
            dc_title: ""                
        }; 
    }
    
    self.create_site = function () {
        ld_util.send_create(self.model._subject,self.new_site_model,function(request){
            if(request.status === 201) {
                var site_model = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
                self.model.ldp_contains.push(site_model);
                self.model = self.model; //triggers UI to be rebuilt
                self.new_site_model = null;
            }
            else {
                siteserver.displayResponse(request, 'error');                                
            }
        });
        
    }
    
    self.cancel_create_site = function () {
        self.error = null;
        self.new_site_model = null;
    }
}
