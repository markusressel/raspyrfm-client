from raspyrfm_client.device_implementations.controlunit.manufacturer.intertechno.CMR1000 import CMR1000


class ITR3500(CMR1000):
    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

        super(CMR1000, self).__init__(Manufacturer.INTERTECHNO, ControlUnitModel.ITR_3500)
