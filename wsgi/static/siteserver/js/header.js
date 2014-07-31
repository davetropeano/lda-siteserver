window.siteserver = window.siteserver || {};

siteserver.HeaderViewModel = function() {
    var self = this;
    self.jwt = misc_util.get_jwt_claims();
    self.cpanel = "";
    
    self.locked_out = function(){
        var is_locked_out = !siteserver.headerVM.jwt.fka;
        return !siteserver.headerVM.jwt.fka;
    };
    
    ko.track(self);  
    
    //load cpanel
    ld_util.get("/",function(request){
        var jso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
        self.cpanel = jso.ce_sites;
    });
    

    $(".alert").alert();
}
