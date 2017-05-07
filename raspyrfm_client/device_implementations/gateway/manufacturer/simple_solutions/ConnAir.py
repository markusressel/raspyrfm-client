from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import Device
from raspyrfm_client.device_implementations.gateway.base import Gateway


class ConnAir(Gateway):
    def __init__(self, host: str = None, port: int = 49880):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
        super().__init__(Manufacturer.SIMPLE_SOLUTIONS, GatewayModel.CONNAIR, host, port)

    def generate_code(self, device: Device, action: Action) -> str:
        """
        This method can be implemented by inheriting classes if it does not implement get_pulse_data
        :param device: The device to generate the code for
        :param action: action to execute
        :return: signal code
        """
        if device.get_channel_config() is None:
            raise ValueError("Missing channel configuration :(")
        if action not in device.get_supported_actions():
            raise ValueError("Unsupported action: " + str(action))

        pulsedata = device.get_pulse_data(action)
        _head_connair = "TXP:0,0,"
        _code = _head_connair
        _code += str(pulsedata[1]) + ','  # add repetitions
        _code += str(5600) + ','
        _code += str(pulsedata[2]) + ','  # add timebase

        _code = _code + str(len(pulsedata[0])) + ','
        for pulse in pulsedata[0]:
            _code += str(pulse[0]) + ','
            _code += str(pulse[1]) + ','
        return _code[:-1]
