from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262DipDevice


class FSS31000W(HX2262DipDevice):
    _h = '0'
    _l = 'f'
    _on = [_h, _l]
    _off = [_l, _h]
    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(FSS31000W, self).__init__(manufacturer_constants.VIVANCO, manufacturer_constants.FSS31000W)