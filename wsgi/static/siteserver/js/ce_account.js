window.siteserver = window.siteserver || {};

siteserver.AccountViewModel = function(){
    var self = this;
    self.account = null;
    self.jwt = misc_util.get_jwt_claims();
    self.register = false;
    self.display = false;
    ko.track(self);
    self.visible = ko.observable(false);    
     
    self.init = function(jso){
        self.showView(jso);
    };
    
    self.showView = function(model) {
        self.account = model;
        if (model.ce_account_id) {
            self.display = true;
        }
        else {
            self.register = true;
        }
        return true;
    };
    
    self.handle_result = function (http) { // specific to this page 
        if (http.status==201) {
            original_url = window.name;
            if (!original_url) {
                original_url = '/';
            }
            else {
                window.name = '';
                window.location.href = original_url;
            }
        }
        else if (http.status==400) {
            document.getElementById('response-message').innerHTML = 'xx' + http.responseText; //todo - parse this out nicely
        }
        else {
            alert('Registration failed unexpectedly. HTTP status/text: ' + http.status + '/' + http.responseText);
            document.getElementById('response-message').innerHTML = 'Registration failed unexpectedly. HTTP status/text: ' + http.status + '/' + http.responseText;
        }
    };
        
    self.validate_and_send = function () { // specific to this page
        var accountId = document.getElementById('accountId').value;
        var password = document.getElementById('password').value;
        var email = document.getElementById('email').value;
        var errors = [];
        if (! accountId) {errors.push('accountId is required');}
        if (! password) {errors.push('password is required');}
        if (! email) {errors.push('email is required');}
        if (errors.length > 0) {
            document.getElementById('response-message').innerHTML = errors.join(", ");
        }
        else {
            var userURL = document.getElementById('userURL').value;
            if (!userURL) // if user did not provide a userURL, default to #owner
                userURL = '#owner';
            var account = {
                'ce_account_id' : accountId,
                'ce_password': password, 
                'vcard_email': email,
                'ce_user': {
                    'rdf_type': new rdf_util.URI(FOAF+'Person'),
                    'foaf_givenName' : document.getElementById('givenName').value,
                    'foaf_familyName' : document.getElementById('familyName').value,
                    'foaf_nick' : document.getElementById('nick').value,
                    '_subject': userURL
                    },
                'vcard_adr': {
                    'rdf_type': new rdf_util.URI(VCARD+'Home'),
                    'vcard_street__address': document.getElementById('street').value,
                    'vcard_locality': document.getElementById('city').value,
                    'vcard_region': document.getElementById('state').value,
                    'vcard_postal__code': document.getElementById('zip').value,
                    'vcard_country__name': document.getElementById('country').value,
                    '_subject': '_:address'
                    },
                'rdf_type': new rdf_util.URI(CE+'Account'),
                '_subject': ''
                }
            var rdf_util_doc = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(account);
            // normally new resources are created via POST, and the server controls the URL of the newly-created resource
            // In the case of accounts, we want to control the URL, so we make up the URL below and use PUT to do the create
            ld_util.send_create(APPLICATION_ENVIRON.initial_simple_jso.ce_account__container, rdf_util_doc, self.handle_result);
        }
    };
}

/*


function AccountViewModel() {
    

    showView(APPLICATION_ENVIRON.initial_simple_jso)
}

ko.applyBindings(new AccountViewModel());
*/