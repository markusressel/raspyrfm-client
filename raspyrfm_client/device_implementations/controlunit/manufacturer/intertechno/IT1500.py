from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import Device


class IT1500(Device):
    _repetitions = 6
    _timebase = 275
    _pausedata = 5600  # not really needed, just for keeping reenginering data

    from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
    from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

    def __init__(self, manufacturer: Manufacturer = Manufacturer.INTERTECHNO,
                 model: ControlUnitModel = ControlUnitModel.IT_1500):
        super().__init__(manufacturer, model)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF]

    def get_channel_config_args(self):
        return {
            'CODE': '[01]{26}$',
            'UNIT': '^([1-9]|0[0-9]|1[1-6])$'
        }

    def get_pulse_data(self, action: Action):
        _sho = 1
        _lon = 5
        _d0 = [(_sho, _sho), (_sho, _lon)]
        _d1 = [(_sho, _lon), (_sho, _sho)]
        _d = (_d0, _d1)  # for bit builders
        _pre = (_sho, 10)
        _post = [(_sho, 41)]

        tuples = [_pre]

        cfg = self.get_channel_config()
        for bit in cfg['CODE']:
            tuples += _d1 if bit == '1' else _d0

        tuples += _d0  # all

        if action is Action.ON:
            tuples += _d1
        elif action is Action.OFF:
            tuples += _d0

        unit = int(cfg['UNIT'])
        for i in range(4):
            tuples += _d1 if unit & 1 << i else _d0

        tuples += _post

        return tuples, self._repetitions, self._timebase
