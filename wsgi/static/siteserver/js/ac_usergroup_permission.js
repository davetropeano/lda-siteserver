window.siteserver = window.siteserver || {}; 

window.siteserver.UserGroupPermissionViewModel = function() {
    var self = this;
    self.jso = {};
    self.userGroups = [];
    self.T = false;
    self.R = false;
    self.C = false;
    self.D = false;
    self.W = false;
    self.X = false;
    self.A = false;
    
    self.get_ac_do = function(){
        var doStr = "";
        doStr += self.A ? '1' : '0';
        doStr += self.X ? '1' : '0';
        doStr += self.W ? '1' : '0';
        doStr += self.D ? '1' : '0';
        doStr += self.C ? '1' : '0';
        doStr += self.R ? '1' : '0';
        doStr += self.T ? '1' : '0';
        var doNum = parseInt(doStr,2);
        return doNum;
    };
    
    self.load_perm_bits = function(doNum){
        var doStr = Number(doNum).toString(2);
        // pad left with zeros
        while(doStr.length < 7) 
            doStr = '0' + doStr;
        self.T = !!+doStr[6];
        self.R = !!+doStr[5];
        self.C = !!+doStr[4];
        self.D = !!+doStr[3];
        self.W = !!+doStr[2];
        self.X = !!+doStr[1];
        self.A = !!+doStr[0];
    };
    
    ko.track(self);
    
    self.init = function(jso){
        self.jso = jso;
        self.load_perm_bits(jso.ac_do);
    };    

    return self;
}
