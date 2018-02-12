from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import ControlUnit


class RC30(ControlUnit):
    _repetitions = 4
    _timebase = 680
    # _pausedata = 80920 µS = 119 steps  # not really needed, just for keeping reenginering data

    from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
    from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

    def __init__(self, manufacturer: Manufacturer = Manufacturer.VOLTCRAFT,
                 model: ControlUnitModel = ControlUnitModel.RC30):
        super().__init__(manufacturer, model)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON, Action.OFF, Action.DIMM, Action.BRIGHT]

    def get_channel_config_args(self):
        return {
            'CODE': '^[01]{12}$',
            'UNIT': '^[1-4]$'
        }

    def get_pulse_data(self, action: Action):
        _d0 = [1, 2]
        _d1 = [2, 1]

        raw = []

        cfg = self.get_channel_config()
        # add 12 bits for housecode
        for bit in cfg['CODE']:
            raw += [1] if bit == '1' else [0]

        unit_code = int(cfg['UNIT'])
        if action in [Action.BRIGHT, Action.DIMM]:
            raw += [1, 1]
        elif unit_code == 1:
            raw += [0, 0]
        elif unit_code == 2:
            raw += [1, 0]
        elif unit_code == 3:
            raw += [0, 1]
        elif unit_code == 4:
            raw += [1, 1]

        raw += [1] if action in [Action.BRIGHT, Action.DIMM] else [0]  # 1 for dim buttons & all-on buttons, else 0

        if action in [Action.ON, Action.DIMM]:
            raw += [1]  # 0 for off / all-off / bright, 1 for on / all-on / dim
        elif action in [Action.OFF, Action.BRIGHT]:
            raw += [0]  # 0 for off / all-off / bright, 1 for on / all-on / dim

        raw += [1] if action in [Action.BRIGHT, Action.DIMM] else [0]  # 1 for dim buttons, else 0
        raw += [0]  # always 0

        # checksum
        raw += [1] if (raw[12] ^ raw[14] ^ raw[16]) != 0 else [0]
        raw += [1] if (raw[13] ^ raw[15] ^ raw[17]) != 0 else [0]

        times = [1]
        for x in raw:
            times += _d1 if x == 1 else _d0
        times += [119]

        tuples = []

        for i in range(0, len(times), 2):
            tuples += [(times[i], times[i + 1])]

        return tuples, self._repetitions, self._timebase
