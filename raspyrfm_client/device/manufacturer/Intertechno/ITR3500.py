from raspyrfm_client.device.manufacturer.Intertechno.CMR1000 import CMR1000


class ITR3500(CMR1000):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(CMR1000, self).__init__(manufacturer_constants.INTERTECHNO, manufacturer_constants.ITR_3500)
