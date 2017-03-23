from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262DipDevice


class Ritter(HX2262DipDevice):
    _l = 'f'
    _h = '0'
    _on = [_l, _l]
    _off = [_h, _h]
    _dips = ['1', '2', '3', '4', '5', '6', 'A', 'B', 'C', 'D']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(Ritter, self).__init__(manufacturer_constants.REV, manufacturer_constants.Ritter)