window.siteserver = window.siteserver || {};

siteserver.SitesViewModel = function(){
    var self = this;
    self.jso = null;
    
    ko.track(self);

    self.visible = ko.observable(false);
    
    self.init = function(jso){
        console.log(jso);
        self.jso = jso;
        if (!self.jso.sites_members)
            self.jso.sites_members = [];
    }
    
    self.new_site = function () {
        console.log('DEBUG THIS');
        window.location = self.sites_container().ce_newMemberInstructions._subject;
        // dispatcher.go_to(self.sites_container().ce_newMemberInstructions._subject, false)
        }
    }
}
