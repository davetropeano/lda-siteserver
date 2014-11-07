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

    self.envVars = ko.observableArray([]);
    self.addKVPair = function() {
        self.envVars.push({key: ko.observable(), value: ko.observable()});
    };
    self.removeKVPair = function(kv) {
        self.envVars.remove(kv);
    }

    // temp variables for editing
    self.improvementLabel = ko.observable();
    self.improvementTitle = ko.observable();
    self.capability = null;

    self.init = function (jso) {
        self.jso = jso;
        self.parentVM = jso.parent;
        self.site_model = self.jso.parent.model;
        self.capabilities = self.jso.ldp_contains ? self.jso.ldp_contains : [];

        // populate envVars by looking for all uppercase attributes in the JSO
        self.envVars = [];
        for (var key in jso) {
            if (jso.hasOwnProperty(key)) {
                var upkey = key.toUpperCase();
                if (upkey == key)
                    self.envVars.push({key: key, value: jso[key]});
            }
        }
    }

    self.showAddImprovementDialog = function(data){
        self.improvementLabel('');
        self.improvementTitle('');
        self.capability = data;

        $('#modal-new-improvement').modal('toggle');
        $('#new-improvement-label').focus();
    }

    self.addImprovement = function(){
        var new_improvement_model = {
            _subject: "",
            rdf_type: self.capability.ce_improvement_type,
            dc_title: self.improvementTitle() ? self.improvementTitle() : self.improvementLabel(),
            rdfs_label: self.improvementLabel(),
            ce_capability: rdf_util.URI(self.capability._subject)
        };

        self.envVars().forEach(function(env) {
            var key = env.key().toUpperCase().replace(/\s+/g, '');
            if (key && key != "") {
                env.key(key);
                new_improvement_model[key] = env.value();
            }
        });

        var post_url = self.capability.ce_improvement_container;
        var ss_session_id = misc_util.getSSSessionId()
        ld_util.send_create(post_url,new_improvement_model,function(request){
            if(request.status === 201) {
                var improvement_model = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
                self.parentVM.add_improvement(improvement_model);
            }
            else {
                siteserver.displayResponse(request,'error');
            }

        }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null); // going cross-origin. Pass SSSESSIONID header to avoid login challenge

        $('#modal-new-improvement').modal('toggle');
    }

    self.navigate_back_to_site = function(){
        ViewManager.switchView(self.site_model);
    }
}
