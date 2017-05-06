from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class RCS1000NComfort(HX2262Compatible):
    _l = 'f'
    _h = '0'
    _on = [_l, _l]
    _off = [_l, _h]
    _repetitions = 5

    from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
    from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

    def __init__(self, manufacturer: Manufacturer = Manufacturer.BRENNENSTUHL,
                 model: ControlUnitModel = ControlUnitModel.RCS_1000_N_COMFORT):
        super(HX2262Compatible, self).__init__(manufacturer, model)

    def get_supported_actions(self) -> [str]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            '1': '^[01]$',
            '2': '^[01]$',
            '3': '^[01]$',
            '4': '^[01]$',
            '5': '^[01]$',
            'CH': '^[A-E]$'
        }

    def get_bit_data(self, action: str):
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
