from raspyrfm_client.device_implementations.controlunit.manufacturer.bat.RC3500_A_IP44_DE import RC3500_A_IP44_DE


class RC_AAA1000_A_IP44_Outdoor(RC3500_A_IP44_DE):
    def __init__(self):
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        super().__init__(Manufacturer.BAT, ControlUnitModel.RC_AAA1000_A_IP44_Outdoor)
