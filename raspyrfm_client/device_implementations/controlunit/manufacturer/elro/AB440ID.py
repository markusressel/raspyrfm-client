from raspyrfm_client.device_implementations.controlunit.manufacturer.elro.AB440S import AB440S


class AB440ID(AB440S):
    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

        super(AB440S, self).__init__(Manufacturer.ELRO, ControlUnitModel.AB440ID)

    def get_channel_config_args(self):
        return {
            '1': '^[01]$',
            '2': '^[01]$',
            '3': '^[01]$',
            '4': '^[01]$',
            '5': '^[01]$',
            'CH': '^[A-C]$'  # device has only switches A-C
        }
