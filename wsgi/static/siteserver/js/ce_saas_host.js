window.siteserver = window.siteserver || {};

siteserver.Saas_hostViewModel = function() {
    var self = this;
    self.visible = ko.observable(false);
    
    self.init = function(jso){
        console.log(jso);
    }
}
