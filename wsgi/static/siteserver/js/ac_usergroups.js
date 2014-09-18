window.siteserver = window.siteserver || {};

siteserver.UserGroupsViewModel = function() {
	
    var self = this;
	self.jso = {};
	self.user_groups = [];
	ko.track(self); 
	self.visible = ko.observable(false);
	
	self.init = function(jso){
    	// Load user_groups
        ld_util.get('/ac',function(response){
            var jso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(response);
            var usrgrps = [];
            for(var i in jso.ldp_member){
                var ug = new siteserver.UserGroupViewModel();
                ug.init(jso.ldp_contains[i]);
                ug.details_toggle();
                usrgrps.push(ug);
            }
            self.user_groups = usrgrps;
        });
    
        // TODO: Load /ac-resource-groups		
	};
}