"use strict";
window.siteserver = window.siteserver || {};

siteserver.SiteViewModel = function () {
    var self = this;
    self.model = null;
    self.new_improvement_model = null;
    self.error = null;
    
    ko.track(self);
    
    self.visible = ko.observable(false);

    self.init = function (jso) {
        self.model = jso;
        if(!self.model.improvements){
            self.model.improvements = [];
        }
        
        console.log(jso);        
    }
    
    self.clearError = function () {
        self.error = null;
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
                console.log("TODO: Handle error");
                //var errors = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
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
}
