from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.manufacturer.universal.HX2262Compatible import HX2262Compatible


class RSL366(HX2262Compatible):
    _h = '0'
    _l = 'f'
    _repetitions = 5

    from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
    from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

    def __init__(self, manufacturer: str = Manufacturer.NONAME, model: str = ControlUnitModel.RSL366):
        super().__init__(manufacturer, model)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            'CODE': '^[1-4]$',
            'CH': '^[1-4]$'
        }

    def get_bit_data(self, action: Action):
        cfg = self.get_channel_config()
        bits = []

        bits += self.calc_match_bits(int(cfg['CODE']) - 1, 4, (self._l, self._h))
        bits += self.calc_match_bits(int(cfg['CH']) - 1, 4, (self._l, self._h))

        bits += [self._l, self._l, self._l]  # fixed

        if action is Action.ON:
            bits += [self._l]
        elif action is Action.OFF:
            bits += [self._h]
        else:
            raise ValueError("Invalid action")

        return bits, self._repetitions
