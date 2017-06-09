from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class CMR1000(HX2262Compatible):
    _l = '0'
    _h = 'f'
    _on = [_h, _h]
    _off = [_h, _l]
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

        super().__init__(Manufacturer.INTERTECHNO, ControlUnitModel.CMR_1000)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            'master': '^[A-P]$',
            'slave': '^([1-9]|[0][1-9]|[1][1-6])$'
        }

    def get_bit_data(self, action: Action):
        cfg = self.get_channel_config()
        bits = []

        master = ord(cfg['master']) - ord('A')
        bits += self.calc_int_bits(master, 4, (self._l, self._h))

        slave = int(cfg['slave']) - 1
        bits += self.calc_int_bits(slave, 4, (self._l, self._h))

        bits += [self._l, self._h]  # fixed

        if action is Action.ON:
            bits += self._on
        elif action is Action.OFF:
            bits += self._off

        return bits, self._repetitions
