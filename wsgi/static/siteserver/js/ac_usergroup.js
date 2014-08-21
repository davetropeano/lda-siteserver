window.siteserver = window.siteserver || {};

siteserver.UserGroupViewModel = function() {
	var self = this;
	self.jso = {};
	self.permissions = [];
	self.details_visible = true;
	self.toggle_style = "glyphicon-minus";
	ko.track(self); 
	self.visible = ko.observable(false);
	
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
	
	self.details_toggle = function(){
	    self.details_visible = !self.details_visible;
	    self.toggle_style = self.details_visible ? 'glyphicon-minus' : 'glyphicon-plus';
	}	
}
