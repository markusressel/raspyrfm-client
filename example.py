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

""" Elro """
print("")
elro_ab440s = rfm_client.get_device(manufacturer_constants.ELRO, manufacturer_constants.AB440S)
print(
    elro_ab440s.get_manufacturer() +
    " " +
    elro_ab440s.get_model() +
    ": " +
    str(elro_ab440s.get_supported_actions()))

elro_ab440s.setup_channel(dips=[False, False, False, False, False, False, False, False, False, False])
print(elro_ab440s.generate_code(actions.ON))
print(elro_ab440s.generate_code(actions.OFF))

""" REV """
print("")

rev_telecontrol = rfm_client.get_device(manufacturer_constants.REV, manufacturer_constants.Telecontrol)

print(
    rev_telecontrol.get_manufacturer() +
    " " +
    rev_telecontrol.get_model() +
    ": " +
    str(rev_telecontrol.get_supported_actions()))

rev_telecontrol.setup_channel(master='A', slave=1)
print(rev_telecontrol.generate_code(actions.ON))
print(rev_telecontrol.generate_code(actions.OFF))

# print(rev_telecontrol.generate_code(actions.DIMM))

rfm_client.send(rev_telecontrol, actions.OFF)

print("")

rev_ritter = rfm_client.get_device(manufacturer_constants.REV, manufacturer_constants.Ritter)

print(
    rev_ritter.get_manufacturer() +
    " " +
    rev_ritter.get_model() +
    ": " +
    str(rev_ritter.get_supported_actions()))

rev_ritter.setup_channel(dips=[False, False, False, False, False, False, False, False, False, False])
print(rev_ritter.generate_code(actions.ON))

""" Intertechno """
print("")

intertechno_cmr_1000 = rfm_client.get_device(manufacturer_constants.INTERTECHNO, manufacturer_constants.CMR_1000)

print(
    intertechno_cmr_1000.get_manufacturer() +
    " " +
    intertechno_cmr_1000.get_model() +
    ": " +
    str(intertechno_cmr_1000.get_supported_actions()))

intertechno_cmr_1000.setup_channel(master='A', slave=1)
print(intertechno_cmr_1000.generate_code(actions.ON))
print(intertechno_cmr_1000.generate_code(actions.OFF))

intertechno_cmr_1000.setup_channel(master='P', slave=16)
print(intertechno_cmr_1000.generate_code(actions.ON))
print(intertechno_cmr_1000.generate_code(actions.OFF))

print("")

intertechno_cmr_500 = rfm_client.get_device(manufacturer_constants.INTERTECHNO, manufacturer_constants.CMR_500)

print(
    intertechno_cmr_500.get_manufacturer() +
    " " +
    intertechno_cmr_500.get_model() +
    ": " +
    str(intertechno_cmr_500.get_supported_actions()))

intertechno_cmr_500.setup_channel(master='A', slave=1)
print(intertechno_cmr_500.generate_code(actions.ON))
print(intertechno_cmr_500.generate_code(actions.OFF))

""" Intertek """
print("")
intertek = rfm_client.get_device(manufacturer_constants.INTERTEK, manufacturer_constants.MODEL_1919361)
print(
    intertek.get_manufacturer() +
    " " +
    intertek.get_model() +
    ": " +
    str(intertek.get_supported_actions()))

intertek.setup_channel(dips=[False, False, False, False, False, False, False, False, False, False])
print(intertek.generate_code(actions.ON))
print(intertek.generate_code(actions.OFF))
