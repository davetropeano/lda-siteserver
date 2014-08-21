var ViewManager = {
    views: [],
    mapper: {},

    addView: function(name, view) {
        this.views.push({name: name, view: view});
    },

    showView: function(name, jso) {
        ko.utils.arrayForEach(this.views, function(v) {
            if (v.name == name) {
                v.view.init(jso);
                v.view.visible(true);
            }
            else
                v.view.visible(false);
        });
    },

    doSwitch: function(map, type, jso) {
        var self = this;
        ko.utils.arrayForEach(map, function(elem) {
            if (elem.type == type)
                self.showView(elem.name, jso)
        });
    },

    switchView: function(jso) {
        var rdf_type = jso.rdf_type.uri_string;

        if (rdf_type == LDP+'DirectContainer') {
            var membership_predicate = "ldp_isMemberOfRelation" in jso ? jso.ldp_isMemberOfRelation.uri_string : jso.ldp_hasMemberRelation.uri_string;
            this.doSwitch(this.mapper.containers, membership_predicate, jso);
        }
        else {
            this.doSwitch(this.mapper.types, rdf_type, jso);
        }

        return true;
    },

    get_resource_and_show_view: function(resource_url, history_tracker) {
        ld_util.get(resource_url, function(request){
            if (request.status==200) {
                var jso = APPLICATION_ENVIRON.rdf_converter.make_simple_jso(request)
                if (ViewManager.switchView(jso)) { // resource accepted
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
        });
    },

    init: function(mapper, namespace, segment_ids) {
        var self = this;

        function capitalize(s) {
            return s[0].toUpperCase() + s.slice(1);
        }

        function create_and_bind_viewmodels(map) {
            ko.utils.arrayForEach(map, function(elem) {
                var vm_name = capitalize(elem.name) + 'ViewModel';

                try {
                    // use javascript reflection to get viewmodel object and create instance
                    var vm = new window[namespace][vm_name]();
                }
                catch(err) {
                    console.log("Error loading vm " + namespace + '.' + vm_name + ': ' + err.message);                    
                }

                ko.applyBindings(vm, document.getElementById('page-' + elem.name));
                self.addView(elem.name, vm);
            });
        }

        this.mapper = mapper;

        var ns = window[namespace];
        create_and_bind_viewmodels(mapper.containers);
        create_and_bind_viewmodels(mapper.types);

        // decide if this single-page-app claims a click on an element
        function claimClick(element) {
            var segments = element.pathname.split('/')
            var result = false;

            if (segments.length > 1) {
                segment_ids.forEach(function(segment_id) {
                    if (segments[1] == segment_id)
                        result = true;
                });
            }

            return result;
        }

        // function is called a) if a user click is claimed b) if a history event happens c) go_to is called on the dispatcher
        var dispatcher = new misc_util.Dispatcher(claimClick, this.get_resource_and_show_view)
        dispatcher.hook_history_and_links();
    }
}

