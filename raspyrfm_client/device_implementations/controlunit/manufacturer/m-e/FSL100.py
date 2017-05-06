from raspyrfm_client.device_implementations.controlunit.manufacturer.noname.RSL366 import RSL366


class FSL100(RSL366):
    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        super(RSL366, self).__init__(Manufacturer.M_E,
                                     ControlUnitModel.FLS100)
