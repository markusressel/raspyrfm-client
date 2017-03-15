from raspyrfm_client.device.manufacturer.bat.RC3500_A_IP44_DE import RC3500_A_IP44_DE


class RC_AAA1000_A_IP44_Outdoor(RC3500_A_IP44_DE):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(RC3500_A_IP44_DE, self).__init__(manufacturer_constants.BAT,
                                               manufacturer_constants.RC_AAA1000_A_IP44_Outdoor)
