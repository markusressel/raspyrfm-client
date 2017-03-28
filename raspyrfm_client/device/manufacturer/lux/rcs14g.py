from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class Rcs14G(HX2262Compatible):
    _on = ['f', 'f']
    _off = ['f', '0']
        
    _codes = [
        ['0', '0', '0', 'f', 'f', '0', 'f', '0', 'f', 'f'],
        ['0', '0', '0', 'f', 'f', 'f', '0', '0', 'f', 'f'],
        ['0', '0', '0', 'f', '0', 'f', 'f', '0', 'f', 'f'],
        ['0', '0', '0', '0', 'f', 'f', 'f', '0', 'f', 'f']
    ]
    
    _repetitions = 5
        

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.LUX_GMBH, manufacturer_constants.RCS_14G)

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def get_channel_config_args(self):
        return {
            'CH': '^[1-4]$'
        }
    
        
    def get_bit_data(self, action: str):
        cfg = self.get_channel_config()
        bits = []
        bits += self._codes[int(cfg['CH']) - 1]
        
        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        return bits, self._repetitions