from raspyrfm_client import RaspyRFMClient
from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer

rfm_client = RaspyRFMClient()

print("Supported Gateways:")
rfm_client.list_supported_gateways()

print("")

print("Supported ControlUnits:")
rfm_client.list_supported_controlunits()

raspyrfm = rfm_client.get_gateway(Manufacturer.SEEGEL_SYSTEME, GatewayModel.RASPYRFM, "192.168.2.10")
itgw = rfm_client.get_gateway(Manufacturer.INTERTECHNO, GatewayModel.ITGW, "192.168.2.70")

brennenstuhl_rcs1000 = rfm_client.get_controlunit(Manufacturer.BRENNENSTUHL,
                                                  ControlUnitModel.RCS_1000_N_COMFORT)
brennenstuhl_rcs1000.set_channel_config(**{
    '1': 1,
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    'CH': 'D'
})

print("")

print(raspyrfm.generate_code(brennenstuhl_rcs1000, Action.ON))
print(itgw.generate_code(brennenstuhl_rcs1000, Action.ON))

print("")

bat = rfm_client.get_controlunit(Manufacturer.BAT,
                                 ControlUnitModel.RC3500_A_IP44_DE)
bat.set_channel_config(**{
    '1': 1,
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    'CH': 'D'
})

print(raspyrfm.generate_code(bat, Action.ON))
print(itgw.generate_code(bat, Action.ON))

# rfm_client.send(itgw, brennenstuhl_rcs1000, Action.ON)


manufacturer = Manufacturer("Intertechno")
model = ControlUnitModel("CMR 1000")

cmr1000 = rfm_client.get_controlunit(manufacturer, model)
cmr1000.set_channel_config(**{
    "master": 'B',
    "slave": 1
})

rfm_client.send(itgw, cmr1000, Action.OFF)
