from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class Rcs14G(HX2262Compatible):
    _on = ['f', 'f']
    _off = ['f', '0']

    _codes = [
        ['0', '0', '0', 'f', 'f', '0', 'f', '0', 'f', 'f'],
        ['0', '0', '0', 'f', 'f', 'f', '0', '0', 'f', 'f'],
        ['0', '0', '0', 'f', '0', 'f', 'f', '0', 'f', 'f'],
        ['0', '0', '0', '0', 'f', 'f', 'f', '0', 'f', 'f']
    ]

    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        super().__init__(Manufacturer.LUX_GMBH, ControlUnitModel.RCS_14G)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            'CH': '^[1-4]$'
        }

    def get_bit_data(self, action: Action):
        cfg = self.get_channel_config()
        bits = []
        bits += self._codes[int(cfg['CH']) - 1]

        if action is Action.ON:
            bits += self._on
        elif action is Action.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")

        return bits, self._repetitions
