from raspyrfm_client.device.manufacturer.noname.RSL366 import RSL366


class FSL100(RSL366):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants        
        super(RSL366, self).__init__(manufacturer_constants.M_E,
                                     manufacturer_constants.FLS100)
