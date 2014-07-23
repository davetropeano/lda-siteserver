
var model = window.siteserver.UserGroupViewModel();
model.init(APPLICATION_ENVIRON.initial_simple_jso);
ko.applyBindings(model);