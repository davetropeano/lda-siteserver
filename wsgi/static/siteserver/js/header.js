window.siteserver = window.siteserver || {};

siteserver.HeaderViewModel = function() {
    var self = this;
    self.jwt = misc_util.get_jwt_claims();
    self.cpanel = "";
    self.message = "Welcome. We're not in alpha, beta, or any other letter in the Greek alphabet. Poke around, marvel at what we've done, and don't expect too much :)";
    self.error = null;
    
    self.locked_out = function(){
        var is_locked_out = !siteserver.headerVM.jwt.fka;
        return !siteserver.headerVM.jwt.fka;
    };
    
    ko.track(self);
    
    self.clear_Error = function () {
        self.error = null;
    }
    
    self.clear_message = function () {
        self.message = null;
    }
    
    //load cpanel
    ld_util.get("/",function(request){
        var jso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
        self.cpanel = jso.ce_sites;
    });
    

    
}
