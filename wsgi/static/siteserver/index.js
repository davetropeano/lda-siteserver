RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
DC = 'http://purl.org/dc/terms/'
CE = 'http://ibm.com/ce/ns#'
SUS = 'http://setupshop.me/ns#'
ALREADY_IN_HISTORY = true

app = new function () { // make a global called app. It's useful for debugging
    var self = this
    //self.jwt = misc_util.get_jwt_claims()

    //self.cpanel = APPLICATION_ENVIRON.initial_simple_jso.ce_sites.uri_string;

}()

ko.applyBindings(app)

