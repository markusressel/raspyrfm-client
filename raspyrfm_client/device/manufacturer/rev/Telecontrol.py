from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class Telecontrol(HX2262Compatible):
    _argchecks = {
        'master': '[A-D]$',
        'slave': '[1-3]$'
    }
    
    _on = ['f', 'f']
    _off = ['0', '0']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(Telecontrol, self).__init__(manufacturer_constants.REV, manufacturer_constants.Telecontrol)

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
            bits.append('1' if cfg['master'] == chr(i + ord('A')) else 'f')
            
        for i in range(3):
            bits.append('1' if cfg['slave'] == str(i + 1) else 'f')
            
        bits += ['0', 'f', 'f'] #fixed
        
        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        super().set_bits(bits)
            
        return super().generate_code()