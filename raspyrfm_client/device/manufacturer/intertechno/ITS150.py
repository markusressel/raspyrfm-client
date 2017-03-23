from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible

class ITS150(HX2262Compatible):
    _argchecks = {
        'CODE': '[A-P]$',
        'GROUP': '[1-4]$',
        'CH': '[1-4]$'
    }
    
    _on = ['f', 'f']
    _off = ['f', '0']
		
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.INTERTECHNO, manufacturer_constants.ITS_150)
				
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
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        super().set_bits(bits)
            
        return super().generate_code()