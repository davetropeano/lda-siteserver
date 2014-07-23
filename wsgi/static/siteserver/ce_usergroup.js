window.siteserver = window.siteserver || {};

window.siteserver.UserGroupViewModel = function() {
	
    var self = this;
	self.jso = {};
	self.permissions = [];
	ko.track(self); 
	
	self.init = function(jso){
		self.jso =jso;
		var perms = [];
		for(var i in jso.ac_may){
		    var perm = new siteserver.UserGroupPermissionViewModel();
		    perm.init(jso.ac_may[i]);
		    perms.push(perm);
		}
		self.permissions = perms;		
	};	
	
	self.showView = function(model) {
        self.init(model);        
        return true;
    }

	return self;
}
