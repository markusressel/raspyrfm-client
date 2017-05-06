from raspyrfm_client.device_implementations.controlunit.manufacturer.intertechno.IT1500 import IT1500


class Hama121938(IT1500):
    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        super().__init__(Manufacturer.HAMA, ControlUnitModel.MODEL_00121938)
