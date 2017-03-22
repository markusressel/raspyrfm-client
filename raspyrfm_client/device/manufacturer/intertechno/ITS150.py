from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible
import re

class ITS150(HX2262Compatible):
    _argchecks = {
        'CODE': '[A-P]$',
        'GROUP': '[1-4]$',
        'CH': '[1-4]$'
    }
		
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.INTERTECHNO, manufacturer_constants.ITS_150)
				
    def set_channel_config(self, **channel_arguments) -> None:
        for arg in self._argchecks:
            if arg not in channel_arguments:
                raise ValueError("arguments should contain key \"CODE\"")
            if re.match(self._argchecks[arg], channel_arguments[arg]) is None:
                raise ValueError("argument \"" + arg + "\" out of range")
 
        self._dips = {}
        
        code = ord(channel_arguments['CODE']) - ord('A')
        self._dips['1'] = 'f' if (code & 1<<0 != 0) else '0'
        self._dips['2'] = 'f' if (code & 1<<1 != 0) else '0'
        self._dips['3'] = 'f' if (code & 1<<2 != 0) else '0'
        self._dips['4'] = 'f' if (code & 1<<3 != 0) else '0'
        
        ch = int(channel_arguments['CH']) - 1
        self._dips['5'] = 'f' if (ch & 1<<0 != 0) else '0'
        self._dips['6'] = 'f' if (ch & 1<<1 != 0) else '0'
        
        grp = int(channel_arguments['GROUP']) - 1
        self._dips['7'] = 'f' if (grp & 1<<0 != 0) else '0'
        self._dips['8'] = 'f' if (grp & 1<<1 != 0) else '0'
        
        self._dips['9'] = '0'
        self._dips['10'] = 'f'
        self._dips['11'] = 'f'

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def generate_code(self, action: str) -> str:
        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)
    
        if action is actions.ON:
            self._dips['12'] = 'f'
        elif action is actions.OFF:
            self._dips['12'] = '0'
        else:
            raise ValueError("Invalid action")
            
        super().set_channel_config(**self._dips)
        return super().generate_code()