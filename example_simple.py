from raspyrfm_client import RaspyRFMClient
from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer import manufacturer_constants

rfm_client = RaspyRFMClient("192.168.2.10")
rfm_client.list_supported_devices()

brennenstuhl_rcs1000 = rfm_client.get_device(manufacturer_constants.BRENNENSTUHL,
                                             manufacturer_constants.RCS_1000_N_COMFORT)
brennenstuhl_rcs1000.set_channel_config(**{
    '1': 1,
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    'CH': 'D'
})

rfm_client.send(brennenstuhl_rcs1000, actions.ON)
