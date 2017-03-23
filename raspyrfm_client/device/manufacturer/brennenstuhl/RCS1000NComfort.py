from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262DipDevice


class RCS1000NComfort(HX2262DipDevice):
    _l = 'f'
    _h = '0'
    _on = [_l, _l]
    _off = [_l, _h]
    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.BRENNENSTUHL, manufacturer_constants.RCS_1000_N_COMFORT)