window.siteserver = window.siteserver || {};

window.siteserver.UserGroupsViewModel = function() {
	
    var self = this;
	self.jso = {};
	self.user_groups = [];
	ko.track(self); 
	
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
	
	return self;
}

var model = window.siteserver.UserGroupsViewModel();
model.init();
ko.applyBindings(model);