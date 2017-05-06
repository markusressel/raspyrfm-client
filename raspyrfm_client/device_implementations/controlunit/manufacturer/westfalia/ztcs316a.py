from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class ZtcS316A(HX2262Compatible):
    _h = '0'
    _l = 'f'
    _on = ['0', '1']
    _off = ['1', '0']
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        super().__init__(Manufacturer.WESTFALIA, ControlUnitModel.ZTC_S316A)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            'A': '^[01]$',
            'B': '^[01]$',
            'C': '^[01]$',
            'D': '^[01]$',
            'E': '^[01]$',
            'F': '^[01]$',
            'CH': '^[1-4]$'
        }

    def get_bit_data(self, action: Action):
        cfg = self.get_channel_config()
        bits = []

        for i in range(6):
            bits += self._h if cfg[chr(i + ord('A'))] == '1' else self._l

        for i in range(4):
            bits += self._h if int(cfg['CH']) == (4 - i) else self._l

        if action is Action.ON:
            bits += self._on
        elif action is Action.OFF:
            bits += self._off

        return bits, self._repetitions
