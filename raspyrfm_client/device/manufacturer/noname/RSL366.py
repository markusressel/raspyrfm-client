from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible
import re

class RSL366(HX2262Compatible):
    _argchecks = {
        'CODE': '[1-4]$',
        'CH': '[1-4]$'
    }
		
    from raspyrfm_client.device.manufacturer import manufacturer_constants
    def __init__(self, manufacturer: str = manufacturer_constants.NONAME, model: str = manufacturer_constants.RSL366):
        super().__init__(manufacturer, model)
				
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
        
        for i in range(4):
            bits.append('0' if cfg['CODE'] == chr(i + ord('1')) else 'f')
            
        for i in range(4):
            bits.append('0' if cfg['CH'] == chr(i + ord('1')) else 'f')
            
        bits += ['f', 'f', 'f'] #fixed
        
        if action is actions.ON:
            bits += ['f']
        elif action is actions.OFF:
            bits += ['0']
        else:
            raise ValueError("Invalid action")
            
        super().set_bits(bits)
            
        return super().generate_code()