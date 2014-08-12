RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
OWL = 'http://www.w3.org/2002/07/owl#'
XSD = 'http://www.w3.org/2001/XMLSchema#'
LDP = 'http://www.w3.org/ns/ldp#'
DC = 'http://purl.org/dc/terms/'
CE = 'http://ibm.com/ce/ns#'
AC = 'http://ibm.com/ce/ac/ns#'
VCARD = 'http://www.w3.org/2006/vcard/ns#'
FOAF = 'http://xmlns.com/foaf/0.1/'


var onload_function = function() {
    var head  = document.getElementsByTagName('head')[0]
    var util_script = document.createElement('script')
    util_script.type= 'text/javascript'
    util_script.src = '/sitedesign/utils.js'

    util_script.onload = function() {
        ld_util.onload({}, '/siteserver/spa.html');
    }
    head.appendChild(util_script)
}

window.addEventListener('DOMContentLoaded', onload_function, false)
