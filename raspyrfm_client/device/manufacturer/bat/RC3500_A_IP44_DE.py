from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.brennenstuhl.RCS1000NComfort import RCS1000NComfort


class RC3500_A_IP44_DE(RCS1000NComfort):
    _l = 'f'
    _h = '0'
    _on = [_h, _l]
    _off = [_l, _h]
    _repetitions = 5

    from raspyrfm_client.device.manufacturer import manufacturer_constants
    def __init__(self, manufacturer: str = manufacturer_constants.BAT, model: str = manufacturer_constants.RC3500_A_IP44_DE):
        super().__init__(manufacturer, model)

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