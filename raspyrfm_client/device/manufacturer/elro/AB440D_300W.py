from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S


class AB440D_300W(AB440S):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.ELRO,
                                     manufacturer_constants.AB440D_300W)
