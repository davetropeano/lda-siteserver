window.siteserver = window.siteserver || {};

siteserver.Saas_hostViewModel = function() {
    var self = this;
    self.visible = ko.observable(false);
    
    self.init = function(jso){
        console.log(jso);
        siteserver.displayResponse(
            "Welcome. We're not in alpha, beta, or any other letter in the Greek alphabet. Poke around, marvel at what we've done, and don't expect too much :)"
        );
    }
}
