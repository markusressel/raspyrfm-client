from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible

class ITS150(HX2262Compatible):
    _argchecks = {
        'CODE': '[A-P]$',
        'GROUP': '[1-4]$',
        'CH': '[1-4]$'
    }
    
    _l = '0'
    _h = 'f'
    
    _on = ['f', 'f']
    _off = ['f', '0']
		
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.INTERTECHNO, manufacturer_constants.ITS_150)
				
    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def get_bits(self, action: str):
        cfg = self.get_channel_config()
        bits = []
        
        code = ord(cfg['CODE']) - ord('A')
        bits += self.calc_int_bits(code, 4)
        
        ch = int(cfg['CH']) - 1
        bits += self.calc_int_bits(ch, 2)
                    
        grp = int(cfg['GROUP']) - 1
        bits += self.calc_int_bits(grp, 2)
            
        bits += ['0', 'f'] #fixed

        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        return bits