from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class ITS150(HX2262Compatible):
    _l = '0'
    _h = 'f'
    _on = [_h, _h]
    _off = [_h, _l]
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.INTERTECHNO, manufacturer_constants.ITS_150)

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]

    def get_channel_config_args(self):
        return {
            'CODE': '^[A-P]$',
            'GROUP': '^[1-4]$',
            'CH': '^[1-4]$'
        }

    def get_bit_data(self, action: str):
        cfg = self.get_channel_config()
        bits = []

        code = ord(cfg['CODE']) - ord('A')
        bits += self.calc_int_bits(code, 4, (self._l, self._h))

        ch = int(cfg['CH']) - 1
        bits += self.calc_int_bits(ch, 2, (self._l, self._h))

        group = int(cfg['GROUP']) - 1
        bits += self.calc_int_bits(group, 4, (self._l, self._h))

        bits += [self._l, self._h]  # fixed

        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off

        return bits, self._repetitions
