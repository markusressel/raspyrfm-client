from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262DipDevice


class Set2605(HX2262DipDevice):
    _h = '0'
    _l = 'f'
    _on = [_l, _l]
    _off = [_l, _h]
    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(Set2605, self).__init__(manufacturer_constants.POLLIN_ELECTRONIC, manufacturer_constants.SET_2605)