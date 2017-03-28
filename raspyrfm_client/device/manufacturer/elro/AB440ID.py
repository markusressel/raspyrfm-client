from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S


class AB440ID(AB440S):
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.ELRO, manufacturer_constants.AB440ID)
        
    def get_channel_config_args(self):
        return {
            '1': '^[01]$',
            '2': '^[01]$',
            '3': '^[01]$',
            '4': '^[01]$',
            '5': '^[01]$',
            'CH': '^[A-C]$' #device as only switches A-C
        }