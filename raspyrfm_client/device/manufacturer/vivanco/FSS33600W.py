from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S
from raspyrfm_client.device.manufacturer.vivanco.FSS31000W import FSS31000W


class FSS33600W(FSS31000W):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.VIVANCO,
                                     manufacturer_constants.FSS33600W)
