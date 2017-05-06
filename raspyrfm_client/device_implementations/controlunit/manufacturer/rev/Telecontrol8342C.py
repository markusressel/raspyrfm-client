from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class Telecontrol(HX2262Compatible):
    _h = '1'
    _l = 'f'
    _on = ['f', 'f']
    _off = ['0', '0']
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

        super(Telecontrol, self).__init__(Manufacturer.REV, ControlUnitModel.TELECONTROL8342C)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            'master': '[A-D]$',
            'slave': '[1-3]$'
        }

    def get_bit_data(self, action: Action):
        cfg = self.get_channel_config()
        bits = []

        for i in range(4):
            bits.append(self._h if cfg['master'] == chr(i + ord('A')) else self._l)

        for i in range(3):
            bits.append(self._h if cfg['slave'] == str(i + 1) else self._l)

        bits += ['0', 'f', 'f']  # fixed

        if action is Action.ON:
            bits += self._on
        elif action is Action.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")

        return bits, self._repetitions
