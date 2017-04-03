from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.intertechno.IT1500 import IT1500

class Hama121938(IT1500):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.HAMA, manufacturer_constants._121938)