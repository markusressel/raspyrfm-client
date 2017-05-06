from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import Device


class Ec000x(Device):
    _on = ['0', '1']
    _off = ['1', '0']

    _lo = 1
    _hi = 3
    _seqLo = [(_lo, _hi)]
    _seqHi = [(_hi, _lo)]
    _sync = [(1, 31)]

    _timebase = 3300
    _pauselen = 5600

    _chvalues = [
        _seqHi + _seqHi + _seqHi,
        _seqLo + _seqHi + _seqHi,
        _seqHi + _seqLo + _seqHi,
        _seqHi + _seqHi + _seqLo
    ]

    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        super().__init__(Manufacturer.LOGILINK, ControlUnitModel.EC000X)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF, Action.PAIR]

    def get_channel_config_args(self):
        return {
            'CODE': '^[0-9A-F]{5}$',
            'CH': '^[1-4]$'
        }

    def get_pulse_data(self, action: Action):
        cfg = self.get_channel_config()
        tuples = []
        for nibble in cfg['CODE']:
            val = int(nibble, 16)
            for i in range(4):
                if (val & 0x8) > 0:
                    tuples += self._seqHi
                else:
                    tuples += self._seqLo
                val <<= 1

        if action is Action.ON:
            tuples += self._seqHi
            repetitions = 5
        elif action is Action.PAIR:
            tuples += self._seqHi
            repetitions = 15
        elif action is Action.OFF:
            tuples += self._seqLo
            repetitions = 5

        tuples += self._chvalues[int(cfg['CH']) - 1]

        tuples += self._sync

        return tuples, repetitions, self._timebase
