from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class ZtcS316A(HX2262Compatible):
    _on = ['f', 'f']
    _off = ['f', '0']
    
    _argchecks = {
        'CH': '[1-4]$'
    }
    
    _codes = [
        ['0', '0', '0', 'f', 'f', '0', 'f', '0', 'f', 'f'],
        ['0', '0', '0', 'f', 'f', 'f', '0', '0', 'f', 'f'],
        ['0', '0', '0', 'f', '0', 'f', 'f', '0', 'f', 'f'],
        ['0', '0', '0', '0', 'f', 'f', 'f', '0', 'f', 'f']
    ]
        

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.LUX_GMBH, manufacturer_constants.RCS_14G)

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]

    def generate_code(self, action: str) -> str:
        cfg = self.get_channel_config()
        if cfg is None:
            raise ValueError("Missing channel configuration :(")
        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)
            
        bits = []
        
        bits += self._codes[int(cfg['CH']) - 1]
        
        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        super().set_bits(bits)
        
        return super().generate_code()