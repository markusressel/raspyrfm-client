from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class AB440S(HX2262Compatible):
    _h = '0'
    _l = 'f'
    _on = [_h, _l]
    _off = [_l, _h]
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

        super().__init__(Manufacturer.ELRO, ControlUnitModel.AB440S)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            '1': '^[01]$',
            '2': '^[01]$',
            '3': '^[01]$',
            '4': '^[01]$',
            '5': '^[01]$',
            'CH': '^[A-D]$'  # manual: DIP switch E may not be used and has to be turned off!
        }

    def get_bit_data(self, action: Action):
        cfg = self.get_channel_config()
        bits = []

        for i in range(5):
            bits += self._h if cfg[str(i + 1)] == '1' else self._l

        ch = ord(cfg['CH']) - ord('A')
        bits += self.calc_match_bits(ch, 5, (self._l, self._h))

        if action is Action.ON:
            bits += self._on
        elif action is Action.OFF:
            bits += self._off

        return bits, self._repetitions
