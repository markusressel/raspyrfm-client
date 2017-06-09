from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
from raspyrfm_client.device_implementations.controlunit.manufacturer.brennenstuhl.RCS1000NComfort import RCS1000NComfort
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer


class RC3500_A_IP44_DE(RCS1000NComfort):
    _l = 'f'
    _h = '0'
    _on = [_h, _l]
    _off = [_l, _h]
    _repetitions = 5

    def __init__(self, manufacturer: Manufacturer = Manufacturer.BAT,
                 model: ControlUnitModel = ControlUnitModel.RC3500_A_IP44_DE):
        super(RCS1000NComfort, self).__init__(manufacturer, model)

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
