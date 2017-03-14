from raspyrfm_client.device.manufacturer.elro import AB440ID


class AB440IS(AB440ID):
    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440ID, self).__init__(manufacturer_constants.ELRO,
                                      manufacturer_constants.AB440IS)
