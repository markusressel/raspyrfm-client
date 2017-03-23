from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262DipDevice


class ZtcS316A(HX2262DipDevice):
    _h = '0'
    _l = 'f'
    _on = ['0', '1']
    _off = ['1', '0']
    _dips = ['A', 'B', 'C', 'D', 'E', 'F', '4', '3', '2', '1']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.WESTFALIA, manufacturer_constants.ZTC_S316A)

    