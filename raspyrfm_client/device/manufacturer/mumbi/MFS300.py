from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device
from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S


class MFS300(AB440S):

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.MUMBI, manufacturer_constants.M_FS300)
