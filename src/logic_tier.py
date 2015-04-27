from ac_logic_tier import Domain_Logic as AC_Domain_Logic
from account_logic_tier import Domain_Logic as account_Domain_Logic
from mt_logic_tier import Domain_Logic as MT_Domain_Logic
import ld4apps.aggregating_logic_tier as base 

class Domain_Logic(base.Domain_Logic):

    def create_logic_tier(self):
        if not self.logic_tier:
            all_parts = self.environ['PATH_INFO'].split('/')
            if all_parts[1] == '' or all_parts[1] == 'mt': 
                self.logic_tier = MT_Domain_Logic(self.environ)
            elif all_parts[1] == 'account': 
                self.logic_tier = account_Domain_Logic(self.environ)
            elif all_parts[1] == 'ac' or all_parts[1].startswith('ac-'): 
                self.logic_tier = AC_Domain_Logic(self.environ)
        return self.logic_tier