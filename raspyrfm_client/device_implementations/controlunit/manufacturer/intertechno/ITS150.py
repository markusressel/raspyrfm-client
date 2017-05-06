from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class ITS150(HX2262Compatible):
    DISABLED = True

    _l = '0'
    _h = 'f'
    _on = [_h, _h]
    _off = [_h, _l]
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        super().__init__(Manufacturer.INTERTECHNO, ControlUnitModel.ITS_150)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            'CODE': '^[A-P]$',
            'GROUP': '^[1-4]$',
            'CH': '^[1-4]$'
        }

    def get_bit_data(self, action: Action):
        cfg = self.get_channel_config()
        bits = []

        code = ord(cfg['CODE']) - ord('A')
        bits += self.calc_int_bits(code, 4, (self._l, self._h))

        ch = int(cfg['CH']) - 1
        bits += self.calc_int_bits(ch, 2, (self._l, self._h))

        group = int(cfg['GROUP']) - 1
        bits += self.calc_int_bits(group, 4, (self._l, self._h))

        bits += [self._l, self._h]  # fixed

        if action is Action.ON:
            bits += self._on
        elif action is Action.OFF:
            bits += self._off

        return bits, self._repetitions
