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
                
        self._channel = channel_arguments
 
    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def generate_code(self, action: str) -> str:
        cfg = self.get_channel_config()
        if cfg is None:
            raise ValueError("Missing channel configuration :(")
        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)
            
        bits = []
        
        code = ord(cfg['CODE']) - ord('A')
        for i in range(4):
            bits.append('f' if (code & 1<<i != 0) else '0')
            
        ch = int(cfg['CH']) - 1
        for i in range(2):
            bits.append('f' if (ch & 1<<i != 0) else '0')
            
        grp = int(cfg['GROUP']) - 1
        for i in range(2):
            bits.append('f' if (grp & 1<<i != 0) else '0')
            
        bits += ['0', 'f'] #fixed

        if action is actions.ON:
            bits += ['f', 'f']
        elif action is actions.OFF:
            bits += ['f', '0']
        else:
            raise ValueError("Invalid action")
            
        super().set_bits(bits)
            
        return super().generate_code()