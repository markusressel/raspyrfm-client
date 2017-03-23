from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262DipDevice


class RC3500_A_IP44_DE(HX2262DipDevice):
    _l = 'f'
    _h = '0'
    _on = [_h, _l]
    _off = [_l, _h]
    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(RC3500_A_IP44_DE, self).__init__(manufacturer_constants.BAT, manufacturer_constants.RC3500_A_IP44_DE)
