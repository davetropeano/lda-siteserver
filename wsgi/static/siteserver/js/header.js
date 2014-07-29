window.siteserver = window.siteserver || {};

siteserver.HeaderViewModel = function() {
    var self = this;
    self.jwt = misc_util.get_jwt_claims();
    self.cpanel = "/mt/sites";
    ko.track(self);        
}
