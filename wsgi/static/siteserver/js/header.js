window.siteserver = window.siteserver || {};

siteserver.HeaderViewModel = function() {
    var self = this;
    self.name = ko.observable();
    self.applications_url = ko.observable();
    self.services_url = ko.observable();
    self.is_set = ko.observable(false);
    self.home = ko.observable(siteserver.SERVER_ROOT + '/xdo/region/systems');
    self.message = ko.observable();
    
    self.init = function(jso){
        console.log(jso);
    }

    self.clearMessage = function() {
        self.message('');
    }

    self.servicesName = ko.computed(function() {
        return self.name() ? self.name() : ' ';
    });
}
