from raspyrfm_client.device_implementations.controlunit.manufacturer.elro.AB440S import AB440S


class FSS31000W(AB440S):
    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        super(AB440S, self).__init__(Manufacturer.VIVANCO, ControlUnitModel.FSS31000W)
