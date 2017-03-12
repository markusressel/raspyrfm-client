from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S


class AB440L(AB440S):
    _s_speed_itgw = "125,"

    _dips = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.ELRO,
                                     manufacturer_constants.AB440L)
