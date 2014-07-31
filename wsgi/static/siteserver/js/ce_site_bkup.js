window.siteserver = window.siteserver || {};


function test(){

    var dispatcher = new misc_util.Dispatcher(
        function(element) { // function is called to decide if this single-page-app claims a click on an element
            var segments = element.pathname.split('/')
            return element.host == window.location.host && segments.length > 1 && segments[1] == 'mt'
            },
        self.get_resource_and_show_view); // function is called a) if a user click is claimed (already_in_history will be false) b) if a history event happens (already_in_history will be true)
    dispatcher.hook_history_and_links();
    
    self.show_view = function (model) {
        /* This is the central dispatcher for the application. It is called every time we change URL within the app. This can happen when:
            1) The user types a URL of one of our resources into the address bar and we enter the app
            2) The user hits a back or forward button or selects from history
            3) The code of our application chooses to navigate to a new URL
            4) The user clicks on an anchor element that referenced the URL. This also has two cases:
                a) The anchor element was created by another application. In that case we are entering this app
                b) The anchor element was create by this app. In that case we will stay within the app and navigate to the right place
            In all cases, by the time we get here, we have already done a GET to fetch the resource from the server and converted the response to a simple Javascript object.
            We are strict about URLs - we do not support the technique where you navigate to a 'fake' URL that does not exist on the server. 'Friends don't let friends fake URLs'
        */
        //if (model.rdf_type == CE+'Saas_host') {
        if (model.rdf_type == LDP+'DirectContainer') {
            self.host_controller(new host_controller(model, self));
            self.site_controller(null);
            self.edit_site_controller(null);
            self.create_site_controller(null);
            self.create_improvement_controller(null);
            }
        else if (model.rdf_type == CE+'Site') {
            self.site_controller(new site_controller(model, self));
            self.host_controller(null);
            self.edit_site_controller(null);
            self.create_site_controller(null);
            self.create_improvement_controller(null);
            }
        else if (model.rdf_type == CE+'NewMemberInstructions' &&  model.ce_newMemberContainer.ldp_hasMemberRelation == CE+'sites') {
            self.site_controller(null);
            self.host_controller(null);
            self.edit_site_controller(null);
            self.create_site_controller(new create_site_controller(model, self));
            self.create_improvement_controller(null);
            }
        else if (model.rdf_type == CE+'NewMemberInstructions' &&  model.ce_newMemberContainer.ldp_hasMemberRelation == CE+'has_improvement') {
            self.site_controller(null);
            self.host_controller(null);
            self.edit_site_controller(null);
            self.create_site_controller(null);
            self.create_improvement_controller(new create_improvement_controller(model, self));
            }
        else {
            return false;
            }
        return true;
    }

    self.enter_edit_mode = function (arg) {
        self.edit_site_controller(self.site_controller())
        self.site_controller(null)
        }
    
    self.enter_create_improvement_mode = function (arg) {
        self.create_improvement_controller(self.site_controller())
        self.site_controller(null)
        }

    self.get_resource_and_show_view = function(resource_url, history_tracker) {
        ld_util.get(resource_url, function(request){
            if (request.status==200) {
                var resource_json = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                if (show_view(resource_json)) { // resource accepted
                    history_tracker.accept_url()
                    }
                else { // we cannot handle this resource
                    history_tracker.decline_url()
                    }
                }
            else if (request.status==401) {
                window.name = resource_url
                var resource_json = JSON.parse(request.responseText)
                window.location.href = resource_json['http://ibm.com/ce/ns#login-page']
                }
            else {
                console.log( request.status )
                }
            })
        }    

    function site_controller(model, parent) {
        var self = this
        self.parent = parent
        self.site = model
        self.improvements = get_improvements(self.site.ce_improvements)
        self.capabilities = get_capabilities()

        function get_capabilities() {
            var result = ko.observableArray()
            var ss_session_id = misc_util.getSSSessionId()
            ld_util.get(self.site.ce_site_capabilities, function(request){
                if (request.status==200) {
                    var capabilities_jso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                    if (capabilities_jso.ldp_contains)
                        result(capabilities_jso.ldp_contains)
                    }
                else {
                    console.log( request.status )
                    }
                }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null) // going cross-origin. Pass SSSESSIONID header to avoid login challenge
            return result
            }

        function get_improvements(improvement_urls) {
            var improvements = ko.observableArray()
            if (improvement_urls) {
                var ss_session_id = misc_util.getSSSessionId()
                for (var i = 0; i<improvement_urls.length; i++) {
                    var improvement_url = improvement_urls[i] //calculate the tenant's domain
                    ld_util.get(improvement_url, function(request) {
                        if (request.status==200) {
                            var improvement = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                            improvements.push(improvement)
                            improvements.sort(function(a,b){
                                return (b.dc_created > a.dc_created) ? -1 : (b.dc_created < a.dc_created) ? 1 : 0
                                })
                            }
                        else {
                            console.log( request.status )
                            }
                        }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null) // going cross-origin. Pass SSSESSIONID header to avoid login challenge
                    }
                }
            return improvements
            }

        self.submit_edit = function() {
            self.update_site({dc_title: self.site.dc_title})
            }

        self.update_site = function(patch) {
            patch['_subject'] = self.site._subject
            var rdf_jso = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(patch)
            ld_util.send_patch(self.site._subject, self.site.ce_modificationCount, rdf_jso, function(http) {
                if (http.status==200) { // update ok
                    parent.last_error('Update OK')
                    }
                else if (http.status==400) {
                    parent.last_error(http.responseText) //todo - parse this out nicely
                    }
                else {
                    alert('Update failed unexpectedly: ' + http.status + '/' + http.responseText)
                    parent.last_error(http.responseText) //todo - parse this out nicely
                    }
                self.cancel_site_mode()
                })
            }

        self.create_improvement = function(capability) {
            var ss_session_id = misc_util.getSSSessionId()
            var new_improvement = {
                _subject: '',
                rdf_type: capability.ce_improvement_type,
                ce_capability: new rdf_util.URI(capability._subject),
                dc_title: ''
                }
            ld_util.send_create(capability.ce_improvement_container, APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(new_improvement), function(http) {
                if (http.status==201) { // create ok
                    var new_improvement_url = new rdf_util.URI(http.getResponseHeader('Location'))
                    if (!self.site.ce_improvements) {
                        self.site.ce_improvements = [new_improvement_url]
                        }
                    else {
                        self.site.ce_improvements.push(new_improvement_url)
                        }
                    self.update_site({ce_improvements: self.site.ce_improvements})
                    }
                else if (http.status==400) {
                    parent.last_error(http.responseText) //todo - parse this out nicely
                    }
                else {
                    alert('Update failed unexpectedly: ' + http.status + '/' + http.responseText)
                    parent.last_error(http.responseText) //todo - parse this out nicely
                    }
                }, ss_session_id ? {'SSSESSIONID': ss_session_id}: null ) // going cross-origin. Pass ss_session_id header to avoid login challenge
            }

        self.cancel_site_mode = function (arg) {
            dispatcher.go_to(self.site._subject, ALREADY_IN_HISTORY)
            }

        }

    function create_site_controller (model, parent) {
        var self = this
        self.parent = parent
        self.site = {
            _subject: '',
            rdf_type: new rdf_util.URI(CE+'Site')
            }
        self.newMemberInstructions = model
        self.create_site = function() {
            var rdf_jso = APPLICATION_ENVIRON.rdf_converter.convert_to_rdf_jso(self.site)
            ld_util.send_create('/mt/sites', rdf_jso, function(http) {
                if (http.status==201) { // create ok
                    parent.last_error('Update OK')
                    self.cancel_create_site()
                    }
                else if (http.status==400) {
                    parent.last_error(http.responseText) //todo - parse this out nicely
                    }
                else {
                    alert('Update failed unexpectedly: ' + http.status + '/' + http.responseText)
                    parent.last_error(http.responseText) //todo - parse this out nicely
                    }
                })
            }

        self.cancel_create_site = function (arg) {
            window.history.back()
            }
        }

    function create_improvement_controller (model, parent) {
        var self = this
        self.parent = parent
        self.newMemberInstructions = model
        self.new_improvement = null
        self.capabilities = get_capabilities()

        self.cancel_create_improvement = function (arg) {
            window.history.back()
            }
        }

    function host_controller (model, parent) {
        var self = this
        self.parent  = parent
        self.saas_host = model
        self.sites_container = ko.observable()
        self.sites_members = ko.observableArray()

        var sites_json = APPLICATION_ENVIRON.initial_simple_jso;
        self.sites_container(sites_json);
        if (sites_json.ldp_contains)
            self.sites_members(sites_json.ldp_contains);

        self.new_site = function () {
            console.log('DEBUG THIS');
            window.location = self.sites_container().ce_newMemberInstructions._subject;
            // dispatcher.go_to(self.sites_container().ce_newMemberInstructions._subject, false)
            }
        }

    }

