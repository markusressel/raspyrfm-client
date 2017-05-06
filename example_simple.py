from raspyrfm_client import RaspyRFMClient
from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer

rfm_client = RaspyRFMClient("192.168.2.10")
rfm_client.list_supported_controlunits()

brennenstuhl_rcs1000 = rfm_client.get_device(Manufacturer.BRENNENSTUHL,
                                             ControlUnitModel.RCS_1000_N_COMFORT)
brennenstuhl_rcs1000.set_channel_config(**{
    '1': 1,
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    'CH': 'D'
})

rfm_client.send(brennenstuhl_rcs1000, Action.ON)
