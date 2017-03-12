from raspyrfm_client import RaspyRFMClient
from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer import manufacturer_constants

""" RaspyRFM Client """
# rfm_client = RaspyRFMClient("192.168.2.40")
rfm_client = RaspyRFMClient()
print(rfm_client.search())

rfm_client.list_supported_devices()

print("Host: " + str(rfm_client.get_host()))
print("Port: " + str(rfm_client.get_port()))
print("Manufacturer: " + str(rfm_client.get_manufacturer()))
print("Model: " + str(rfm_client.get_model()))
print("Firmware: " + str(rfm_client.get_firmware_version()))

""" Brennenstuhl """
print("")

brennenstuhl_rcs1000 = rfm_client.get_device(manufacturer_constants.BRENNENSTUHL,
                                             manufacturer_constants.RCS_1000_N_COMFORT)
brennenstuhl_rcs1000.setup_channel(**{
    '1': False,
    '2': False,
    '3': False,
    '4': False,
    '5': False,
    'A': False,
    'B': False,
    'C': False,
    'D': False,
    'E': False
})

print(str(brennenstuhl_rcs1000))

print(brennenstuhl_rcs1000.generate_code(actions.ON))
print(brennenstuhl_rcs1000.generate_code(actions.OFF))

""" Elro """
print("")
elro_ab440s = rfm_client.get_device(manufacturer_constants.ELRO, manufacturer_constants.AB440S)

elro_ab440s.setup_channel(**{
    '1': False,
    '2': False,
    '3': False,
    '4': False,
    '5': False,
    'A': False,
    'B': False,
    'C': False,
    'D': False,
    'E': False
})

print(str(elro_ab440s))

print(elro_ab440s.generate_code(actions.ON))
print(elro_ab440s.generate_code(actions.OFF))

""" REV """
print("")

rev_telecontrol = rfm_client.get_device(manufacturer_constants.REV, manufacturer_constants.Telecontrol)

rev_telecontrol.setup_channel(master='A', slave=1)

print(str(rev_telecontrol))

print(rev_telecontrol.generate_code(actions.ON))
print(rev_telecontrol.generate_code(actions.OFF))

rfm_client.send(rev_telecontrol, actions.ON)

print("")

rev_ritter = rfm_client.get_device(manufacturer_constants.REV, manufacturer_constants.Ritter)

rev_ritter.setup_channel(**{
    '1': False,
    '2': False,
    '3': False,
    '4': False,
    '5': False,
    '6': False,
    'A': False,
    'B': False,
    'C': False,
    'D': False
})

print(str(rev_ritter))

print(rev_ritter.generate_code(actions.ON))

""" Intertechno """
print("")

intertechno_cmr_1000 = rfm_client.get_device(manufacturer_constants.INTERTECHNO, manufacturer_constants.CMR_1000)

intertechno_cmr_1000.setup_channel(master='A', slave=1)

print(str(intertechno_cmr_1000))

print(intertechno_cmr_1000.generate_code(actions.ON))
print(intertechno_cmr_1000.generate_code(actions.OFF))

intertechno_cmr_1000.setup_channel(master='P', slave=16)
print(intertechno_cmr_1000.generate_code(actions.ON))
print(intertechno_cmr_1000.generate_code(actions.OFF))

print("")

intertechno_cmr_500 = rfm_client.get_device(manufacturer_constants.INTERTECHNO, manufacturer_constants.CMR_500)

intertechno_cmr_500.setup_channel(master='A', slave=1)

print(str(intertechno_cmr_500))

print(intertechno_cmr_500.generate_code(actions.ON))
print(intertechno_cmr_500.generate_code(actions.OFF))

""" Intertek """
print("")
intertek = rfm_client.get_device(manufacturer_constants.INTERTEK, manufacturer_constants.MODEL_1919361)

intertek.setup_channel(**{
    '1': False,
    '2': False,
    '3': False,
    '4': False,
    '5': False,
    'A': False,
    'B': False,
    'C': False,
    'D': False,
    'E': False
})

print(str(intertek))

print(intertek.generate_code(actions.ON))
print(intertek.generate_code(actions.OFF))
