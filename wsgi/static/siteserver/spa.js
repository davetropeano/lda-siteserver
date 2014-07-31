;(function(window) {
    "use strict";
    window.siteserver = window.siteserver || {}; // xdo is our top level module context
    
    // TODO: SERVER_ROOT needs to be a config option for mobile but read for desktop browsers
    siteserver.SERVER_ROOT = document.location.origin;
    
    siteserver.displayResponse = function(response) {
        var text = '';
        if (response.getResponseHeader('Content-Type') == 'application/json') {
            var json = JSON.parse(response.responseText);
            for (var i = 0; i < json.length; i++) {
                if (json[i][0]) {
                    text += '<b>Bad field: </b>' + json[i][0] + '<b> Error message: </b>';
                }
                text += json[i][1] + '<br>';
            }
        }
        else {
            text = response.responseText;
        }
        siteserver.headerVM.message(text);
        console.log(response);
    }

    //
    // The mapper hash uses a convention over configuration approach to create, bind, and track viewmodels
    //
    // A hash with a name of 'xyz' should have a viewmodel function XyzViewModel, and an HTML div id of page-xyz
    // Viewmodel function objects are contained within a namespace which is passed into ViewManager.init
    //
    // For example, in the namespace xdo the hash element with name 'systems' means there is an xdo.SystemsViewModel function object
    //
    
    var mapper = {
        containers: [
            {name: 'sites', type: CE+'sites'}
            //,{name: 'saas_host', type: CE+'has_service'}
        ],
        types: [
            {name: 'site', type: CE+'Site'},
            {name: 'saas_host', type: CE+'Saas_host'},
            {name: 'login', type: CE+'Login'},
            {name: 'account', type: CE+'Account'}
        ]
    };
    ViewManager.init(mapper, 'siteserver', ['siteserver']);

    //
    // The header and footer VM is special - it doesn't have a container/type associated with it
    // consider modifying viewmodel code to handle this condition
    //
    siteserver.headerVM = new siteserver.HeaderViewModel();
    ko.applyBindings(siteserver.headerVM, document.getElementById('site-header'));
    ko.applyBindings(siteserver.headerVM, document.getElementById('site-notifications'));
    
    siteserver.footerVM = new siteserver.FooterViewModel();
    ko.applyBindings(siteserver.headerVM, document.getElementById('site-footer'));
    
    siteserver.footerVM = new siteserver.FooterViewModel();
    
    
    var jso = APPLICATION_ENVIRON.initial_simple_jso;
    ViewManager.switchView(jso);    
    
}(window));
