from raspyrfm_client.device.manufacturer.vivanco import FSS31000W


class FSS33600W(FSS31000W):
    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(FSS31000W, self).__init__(manufacturer_constants.VIVANCO,
                                        manufacturer_constants.FSS33600W)
