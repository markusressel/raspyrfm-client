from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class AB440S(HX2262Compatible):
    _h = '0'
    _l = 'f'
    _on = [_h, _l]
    _off = [_l, _h]
    _repetitions = 5
    
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.ELRO, manufacturer_constants.AB440S)
                
    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def get_channel_config_args(self):
        return {
            '1': '^[01]$',
            '2': '^[01]$',
            '3': '^[01]$',
            '4': '^[01]$',
            '5': '^[01]$',
            'CH': '^[A-D]$' #manual: DIP switch E may not be used and has to be turned off!
        }
        
    def get_bit_data(self, action: str):
        cfg = self.get_channel_config()
        bits = []
        
        for i in range(5):
            bits += self._h if cfg[str(i + 1)] == '1' else self._l
            
        ch = ord(cfg['CH']) - ord('A')
        bits += self.calc_match_bits(ch, 5, (self._l, self._h))
        
        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
            
        return bits, self._repetitions