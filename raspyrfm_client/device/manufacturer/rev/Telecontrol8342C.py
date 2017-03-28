from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class Telecontrol(HX2262Compatible):
    _h = '1'
    _l = 'f'
    _on = ['f', 'f']
    _off = ['0', '0']
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(Telecontrol, self).__init__(manufacturer_constants.REV, manufacturer_constants.TELECONTROL8342C)

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def get_channel_config_args(self):
        return {
            'master': '[A-D]$',
            'slave': '[1-3]$'
        }

    def get_bit_data(self, action: str):
        cfg = self.get_channel_config()     
        bits = []
        
        for i in range(4):
            bits.append(self._h if cfg['master'] == chr(i + ord('A')) else self._l)
            
        for i in range(3):
            bits.append(self._h if cfg['slave'] == str(i + 1) else self._l)
            
        bits += ['0', 'f', 'f'] #fixed
        
        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        return bits, self._repetitions
