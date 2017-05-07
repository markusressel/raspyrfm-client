from raspyrfm_client import RaspyRFMClient
from raspyrfm_client.device_implementations.controlunit import controlunit_constants, actions

""" RaspyRFM Client """
rfm_client = RaspyRFMClient("192.168.2.10")
# rfm_client = RaspyRFMClient()
# print(rfm_client.search())

rfm_client.list_supported_controlunits()

print("Host: " + str(rfm_client.get_host()))
print("Port: " + str(rfm_client.get_port()))
print("Manufacturer: " + str(rfm_client.get_manufacturer()))
print("Model: " + str(rfm_client.get_model()))
print("Firmware: " + str(rfm_client.get_firmware_version()))

""" Brennenstuhl """
print("")

brennenstuhl_rcs1000 = rfm_client.get_controlunit(controlunit_constants.BRENNENSTUHL,
                                                  controlunit_constants.RCS_1000_N_COMFORT)
brennenstuhl_rcs1000.set_channel_config(**{
    '1': 1,
    '2': 1,
    '3': 1,
    '4': 1,
    '5': 1,
    'CH': 'D'
})

print(str(brennenstuhl_rcs1000))

print(brennenstuhl_rcs1000.generate_code(actions.ON))
print(brennenstuhl_rcs1000.generate_code(actions.OFF))
rfm_client.send(brennenstuhl_rcs1000, actions.ON)

""" Elro """
print("")

elro_ab440id = rfm_client.get_controlunit(controlunit_constants.ELRO, controlunit_constants.AB440ID)

elro_ab440id.set_channel_config(**{
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    'CH': 'A'
})

print(str(elro_ab440id))

print(elro_ab440id.generate_code(actions.ON))
print(elro_ab440id.generate_code(actions.OFF))

print("")
elro_ab440s = rfm_client.get_controlunit(controlunit_constants.ELRO, controlunit_constants.AB440S)

elro_ab440s.set_channel_config(**{
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    'CH': 'A'
})

print(str(elro_ab440s))

print(elro_ab440s.generate_code(actions.ON))
print(elro_ab440s.generate_code(actions.OFF))

""" rev """
print("")

rev_telecontrol = rfm_client.get_controlunit(controlunit_constants.REV, controlunit_constants.TELECONTROL8342C)

rev_telecontrol.set_channel_config(master='A', slave=1)

print(str(rev_telecontrol))

print(rev_telecontrol.generate_code(actions.ON))
print(rev_telecontrol.generate_code(actions.OFF))

rfm_client.send(rev_telecontrol, actions.ON)

print("")

rev_ritter = rfm_client.get_controlunit(controlunit_constants.REV, controlunit_constants.RITTER)

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

print(rev_ritter.generate_code(actions.ON))

""" intertechno """
print("")

intertechno_cmr_1000 = rfm_client.get_controlunit(controlunit_constants.INTERTECHNO, controlunit_constants.CMR_1000)

intertechno_cmr_1000.set_channel_config(master='A', slave=1)

print(str(intertechno_cmr_1000))

print(intertechno_cmr_1000.generate_code(actions.ON))
print(intertechno_cmr_1000.generate_code(actions.OFF))

intertechno_cmr_1000.set_channel_config(master='P', slave=16)
print(intertechno_cmr_1000.generate_code(actions.ON))
print(intertechno_cmr_1000.generate_code(actions.OFF))

print("")

intertechno_cmr_500 = rfm_client.get_controlunit(controlunit_constants.INTERTECHNO, controlunit_constants.CMR_500)

intertechno_cmr_500.set_channel_config(master='A', slave=1)

print(str(intertechno_cmr_500))

print(intertechno_cmr_500.generate_code(actions.ON))
print(intertechno_cmr_500.generate_code(actions.OFF))

""" Intertek """
print("")
intertek = rfm_client.get_controlunit(controlunit_constants.INTERTEK, controlunit_constants.MODEL_1919361)

intertek.set_channel_config(**{
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    'CH': 'A'
})

print(str(intertek))

print(intertek.generate_code(actions.ON))
print(intertek.generate_code(actions.OFF))

""" Intertechno ITS-150 """
print("")
its150 = rfm_client.get_controlunit(controlunit_constants.INTERTECHNO, controlunit_constants.ITS_150)

its150.set_channel_config(**{
    'CODE': 'I',  # house code A-P
    'GROUP': '2',  # group 1-4
    'CH': '1'  # channel (key) 1-4
})

print(str(its150))
rfm_client.send(its150, actions.ON)
