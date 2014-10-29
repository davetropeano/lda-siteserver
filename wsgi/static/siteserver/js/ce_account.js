window.siteserver = window.siteserver || {};

siteserver.AccountViewModel = function(){
    var self = this;
    self.account = null;
    self.register = false;
    self.display = false;
    ko.track(self);
    self.visible = ko.observable(false);
     
    self.init = function(jso){
        //some accounts don't have this (like admin) and it causes errors in the view
        if(!jso.vcard_adr){
            jso.vcard_adr = {
                    vcard_street__address: null,
                    vcard_locality: null,
                    vcard_region: null,
                    vcard_postal__code: null,
                    vcard_country__name: null
            };
        }
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
    
    self.handle_result = function (response) { // specific to this page 
        if (response.status==201) {
            window.location = '/';
            return;
            original_url = window.name;
            if (!original_url) {
                original_url = '/';
            }
            else {
                window.name = '';
                window.location.href = original_url;
            }
        }
        else {
            siteserver.displayResponse(response, 'error');
        }
    };
        
    self.validate_and_send = function () { // specific to this page
        var accountId = document.getElementById('accountId').value;
        var password = document.getElementById('password').value;
        //var email = document.getElementById('email').value;
        var email = 'test@test.com';
        var errors = [];
        //if (!password != password2){errors.push('passwords are not the same');}
        if (! accountId) {errors.push('accountId is required');}
        if (! password) {errors.push('password is required');}
        if (! email) {errors.push('email is required');}
        if (errors.length > 0) {
            ubo.headerVM.displayResponse(errors.join(", "), 'error');
        }
        else {
            var userURL = '#owner';
            var account = {
                'ce_account_id' : accountId,
                'ce_password': password, 
                'vcard_email': email,
                'ce_user': {
                    'rdf_type': new rdf_util.URI(FOAF+'Person'),
                    'foaf_givenName' : '',
                    'foaf_familyName' : '',
                    'foaf_nick' : '',
                    '_subject': userURL
                    },
                'vcard_adr': {
                    'rdf_type': new rdf_util.URI(VCARD+'Home'),
                    'vcard_street__address': '',
                    'vcard_locality': '',
                    'vcard_region': '',
                    'vcard_postal__code': '',
                    'vcard_country__name': '',
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
