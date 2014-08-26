window.siteserver = window.siteserver || {};

siteserver.HeaderViewModel = function() {
    var self = this;
    self.jwt = misc_util.get_jwt_claims();
    self.cpanel = "";
    self.message = "";
    self.message_class = "alert-info";
    
    self.locked_out = function(){
        return !siteserver.headerVM.jwt.fka;
    };
    
    ko.track(self);
    
    self.clear_message = function () {
        self.message = null;
        self.message_class = 'alert-info';
    }
    
    //load cpanel
    ld_util.get("/",function(request){
        var jso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request);
        self.cpanel = jso.ce_sites;
    });
    

    
}
