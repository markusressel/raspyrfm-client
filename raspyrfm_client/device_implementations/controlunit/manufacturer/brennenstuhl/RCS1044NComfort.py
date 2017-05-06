from raspyrfm_client.device_implementations.controlunit.manufacturer.brennenstuhl.RCS1000NComfort import RCS1000NComfort


class RCS1044NComfort(RCS1000NComfort):
    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

        super(RCS1000NComfort, self).__init__(Manufacturer.BRENNENSTUHL,
                                              ControlUnitModel.RCS_1044_N_COMFORT)
