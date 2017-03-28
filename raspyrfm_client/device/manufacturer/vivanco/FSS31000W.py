from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S


class FSS31000W(AB440S):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.VIVANCO, manufacturer_constants.FSS31000W)
