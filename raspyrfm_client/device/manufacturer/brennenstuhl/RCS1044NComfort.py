from raspyrfm_client.device.manufacturer.brennenstuhl.RCS1000NComfort import RCS1000NComfort


class RCS1044NComfort(RCS1000NComfort):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(RCS1000NComfort, self).__init__(manufacturer_constants.BRENNENSTUHL,
                                              manufacturer_constants.RCS_1044_N_COMFORT)
