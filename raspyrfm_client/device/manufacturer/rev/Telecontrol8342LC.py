from raspyrfm_client.device.manufacturer.intertechno.IT1500 import IT1500


class IT1500(IT1500):    
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.REV, manufacturer_constants.TELECONTROL8342LC)
    