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

/*
var onload_function = function() {

    var prefixes = {}
        prefixes[RDFS] = 'rdfs'
        prefixes[RDF] = 'rdf'
        prefixes[LDP] = 'ldp'
        prefixes[XSD] = 'xsd'
        prefixes[DC] = 'dc'
        prefixes[CE] = 'ce'
        prefixes[OWL] = 'owl'
        prefixes[AC] = 'ac'
        prefixes[VCARD] = 'vcard'
        prefixes[FOAF] = 'foaf'

    var type_to_theme_map = {}
        type_to_theme_map[CE+'Site'] = '/siteserver/ce_saas_host.html'
        type_to_theme_map[CE+'Saas_host'] = '/siteserver/index.html'
        //type_to_theme_map[CE+'Saas_host'] = '/siteserver/ce_saas_host.html'
        type_to_theme_map[CE+'Login'] = '/siteserver/ce_login.html'
        type_to_theme_map[CE+'Account'] = '/siteserver/ce_account.html'

    var predicate_to_theme_map = {}
        predicate_to_theme_map[CE+'sites'] = '/siteserver/ce_saas_host.html'
        predicate_to_theme_map[CE+'has_service'] = '/siteserver/ce_saas_host.html'

    var head  = document.getElementsByTagName('head')[0]
    var util_script = document.createElement('script')
    util_script.type= 'text/javascript'
    util_script.src = '/sitedesign/utils.js'
    util_script.onload = function() {ld_util.onload(prefixes, type_to_theme_map, predicate_to_theme_map)}
    head.appendChild(util_script)
    }

window.addEventListener('DOMContentLoaded', onload_function, false)
*/