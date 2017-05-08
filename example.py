from raspyrfm_client import RaspyRFMClient
from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer

""" RaspyRFM Client """
rfm_client = RaspyRFMClient()

rfm_client.list_supported_controlunits()

raspyrfm = rfm_client.get_gateway(Manufacturer.SEEGEL_SYSTEME, GatewayModel.RASPYRFM, "192.168.2.10")

print("Host: " + str(raspyrfm.get_host()))
print("Port: " + str(raspyrfm.get_port()))
print("Manufacturer: " + str(raspyrfm.get_manufacturer()))
print("Model: " + str(raspyrfm.get_model()))
print("Firmware: " + str(raspyrfm.get_firmware_version()))

""" Brennenstuhl """
print("")

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

print(str(brennenstuhl_rcs1000))

print(raspyrfm.generate_code(brennenstuhl_rcs1000, Action.ON))
print(raspyrfm.generate_code(brennenstuhl_rcs1000, Action.OFF))
rfm_client.send(raspyrfm, brennenstuhl_rcs1000, Action.ON)

""" Elro """
print("")

elro_ab440id = rfm_client.get_controlunit(Manufacturer.ELRO, ControlUnitModel.AB440ID)

elro_ab440id.set_channel_config(**{
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    'CH': 'A'
})

print(str(elro_ab440id))

print(raspyrfm.generate_code(elro_ab440id, Action.ON))
print(raspyrfm.generate_code(elro_ab440id, Action.OFF))

print("")
elro_ab440s = rfm_client.get_controlunit(Manufacturer.ELRO, ControlUnitModel.AB440S)

elro_ab440s.set_channel_config(**{
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    'CH': 'A'
})

print(str(elro_ab440s))

print(raspyrfm.generate_code(elro_ab440s, Action.ON))
print(raspyrfm.generate_code(elro_ab440s, Action.OFF))

""" rev """
print("")

rev_telecontrol = rfm_client.get_controlunit(Manufacturer.REV, ControlUnitModel.TELECONTROL8342C)

rev_telecontrol.set_channel_config(master='A', slave=1)

print(str(rev_telecontrol))

print(raspyrfm.generate_code(rev_telecontrol, Action.ON))
print(raspyrfm.generate_code(rev_telecontrol, Action.OFF))

rfm_client.send(raspyrfm, rev_telecontrol, Action.ON)

print("")

rev_ritter = rfm_client.get_controlunit(Manufacturer.REV, ControlUnitModel.RITTER)

rev_ritter.set_channel_config(**{
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    '6': 0,
    'CH': 'A'
})

print(str(rev_ritter))

print(raspyrfm.generate_code(rev_ritter, Action.ON))

""" intertechno """
print("")

intertechno_cmr_1000 = rfm_client.get_controlunit(Manufacturer.INTERTECHNO, ControlUnitModel.CMR_1000)

intertechno_cmr_1000.set_channel_config(master='A', slave=1)

print(str(intertechno_cmr_1000))

print(raspyrfm.generate_code(intertechno_cmr_1000, Action.ON))
print(raspyrfm.generate_code(intertechno_cmr_1000, Action.OFF))

intertechno_cmr_1000.set_channel_config(master='P', slave=16)

print(raspyrfm.generate_code(intertechno_cmr_1000, Action.ON))
print(raspyrfm.generate_code(intertechno_cmr_1000, Action.OFF))

print("")

intertechno_cmr_500 = rfm_client.get_controlunit(Manufacturer.INTERTECHNO, ControlUnitModel.CMR_500)

intertechno_cmr_500.set_channel_config(master='A', slave=1)

print(str(intertechno_cmr_500))

print(raspyrfm.generate_code(intertechno_cmr_500, Action.ON))
print(raspyrfm.generate_code(intertechno_cmr_500, Action.OFF))

""" Intertek """
print("")
intertek = rfm_client.get_controlunit(Manufacturer.INTERTEK, ControlUnitModel.MODEL_1919361)

intertek.set_channel_config(**{
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    'CH': 'A'
})

print(str(intertek))

print(raspyrfm.generate_code(intertek, Action.ON))
print(raspyrfm.generate_code(intertek, Action.OFF))

""" Intertechno ITS-150 """
print("")
its150 = rfm_client.get_controlunit(Manufacturer.INTERTECHNO, ControlUnitModel.ITS_150)

its150.set_channel_config(**{
    'CODE': 'I',  # house code A-P
    'GROUP': '2',  # group 1-4
    'CH': '1'  # channel (key) 1-4
})

print(str(its150))
rfm_client.send(raspyrfm, its150, Action.ON)
