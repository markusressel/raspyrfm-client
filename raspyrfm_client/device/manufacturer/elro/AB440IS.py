from raspyrfm_client.device.manufacturer.elro.AB440ID import AB440ID


class AB440IS(AB440ID):
    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C']

    def __init__(self):
        super(AB440ID, self).__init__()

        from raspyrfm_client.device.manufacturer import manufacturer_constants
        self._model = manufacturer_constants.AB440IS
