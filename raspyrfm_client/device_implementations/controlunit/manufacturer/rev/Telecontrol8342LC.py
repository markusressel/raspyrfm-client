from raspyrfm_client.device_implementations.controlunit.manufacturer.intertechno.IT1500 import IT1500


class Telecontrol2(IT1500):
    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

        super(IT1500, self).__init__(Manufacturer.REV, ControlUnitModel.TELECONTROL8342LC)
