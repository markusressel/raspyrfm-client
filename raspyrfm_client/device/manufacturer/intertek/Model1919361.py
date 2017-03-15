from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S


class Model1919361(AB440S):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.INTERTEK, manufacturer_constants.MODEL_1919361)
