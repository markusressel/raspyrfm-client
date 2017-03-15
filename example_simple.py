from raspyrfm_client import RaspyRFMClient
from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer import manufacturer_constants

rfm_client = RaspyRFMClient("192.168.2.10")

brennenstuhl_rcs1000 = rfm_client.get_device(manufacturer_constants.BRENNENSTUHL,
                                             manufacturer_constants.RCS_1000_N_COMFORT)
brennenstuhl_rcs1000.set_channel_config(**{
    '1': True,
    '2': True,
    '3': True,
    '4': True,
    '5': True,
    'A': False,
    'B': False,
    'C': False,
    'D': True,
    'E': False
})

rfm_client.send(brennenstuhl_rcs1000, actions.ON)
