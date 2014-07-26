window.siteserver = window.siteserver || {};

window.siteserver.LoginViewModel = function(){
    var self = this;
    self.jwt = {};
    self.visible = ko.observable(false);
    
    self.init = function(jso){
        console.log(jso);
    }
    
    self.handle_result = function(http) { // specific to this page 
        if (http.status==200) {
            original_url = window.name;
            if (! original_url) {
                original_url = '/';
            }
            else {
                window.name = '';
            }
            location.assign(original_url);
        }
        else if (http.status==404) {
            document.getElementById('response-message').innerHTML = 'accountId and password not found';
        }
        else
            {document.getElementById('response-message').innerHTML = 'Logon failed unexpectedly. HTTP status/text: ' + http.status + '/' + http.responseText;
        }
    };

    self.validate_and_send = function() { // specific to this page
        var accountId = document.getElementById('accountId').value;
        var password = document.getElementById('password').value;
        var errors = [];
        if (! accountId) {errors.push('accountId is required');}
        if (! password) {errors.push('password is required');}
        if (errors.length > 0) {
            document.getElementById('response-message').innerHTML = errors.join(", ");
        }
        else {
            var login = {
                'ce_account_id': accountId,
                'ce_password': password,
                '_subject': '_:bnode1'
                };
            var rdf_jso = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(login);
            ld_util.send_transform(APPLICATION_ENVIRON.initial_rdf_jso.graph_url, rdf_jso, handle_result);
        }
        return false;
    };

    self.get_registration_form = function() {       
        location.assign(APPLICATION_ENVIRON.initial_simple_jso.ce_registration__page);
        return false;
    };    
};

