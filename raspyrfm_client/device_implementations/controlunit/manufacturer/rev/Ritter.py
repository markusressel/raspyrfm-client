from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class Ritter(HX2262Compatible):
    _l = 'f'
    _h = '0'
    _on = [_l, _l]
    _off = [_h, _h]
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

        super(Ritter, self).__init__(Manufacturer.REV, ControlUnitModel.RITTER)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            '1': '^[01]$',
            '2': '^[01]$',
            '3': '^[01]$',
            '4': '^[01]$',
            '5': '^[01]$',
            '6': '^[01]$',
            'CH': '^[A-D]$'
        }

    def get_bit_data(self, action: Action):
        cfg = self.get_channel_config()
        bits = []

        for i in range(6):
            bits.append(self._h if cfg[str(i + 1)] == '1' else self._l)

        for i in range(4):
            bits.append(self._h if cfg['CH'] == chr(i + ord('A')) else self._l)

        if action is Action.ON:
            bits += self._on
        elif action is Action.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")

        return bits, self._repetitions
