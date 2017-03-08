"""
TODO:

Example usage can be found in the example.py file
"""
from raspyrfm_client.device.base import Device
from raspyrfm_client.device.manufacturer import manufacturer_constants
from raspyrfm_client.device.manufacturer.Intertechno.CMR1000 import CMR1000
from raspyrfm_client.device.manufacturer.Intertechno.CMR1224 import CMR1224
from raspyrfm_client.device.manufacturer.Intertechno.CMR300 import CMR300
from raspyrfm_client.device.manufacturer.Intertechno.CMR500 import CMR500
from raspyrfm_client.device.manufacturer.Intertechno.GRR300 import GRR300
from raspyrfm_client.device.manufacturer.Intertechno.ITR300 import ITR300
from raspyrfm_client.device.manufacturer.Intertechno.ITR3500 import ITR3500
from raspyrfm_client.device.manufacturer.Intertechno.PA31000 import PA31000
from raspyrfm_client.device.manufacturer.Intertechno.PAR1500 import PAR1500
from raspyrfm_client.device.manufacturer.Intertechno.YCR1000 import YCR1000
from raspyrfm_client.device.manufacturer.REV.Ritter import Ritter
from raspyrfm_client.device.manufacturer.REV.Telecontrol import Telecontrol

import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST


class RaspyRFMClient:
    """
    This class is the main interface for generating and sending signals.
    """

    """
    This dictionary maps manufacturer and model constants to their implementation class
    """
    __manufacturer_model_dict = {
        manufacturer_constants.REV: {
            manufacturer_constants.Telecontrol: Telecontrol,
            manufacturer_constants.Ritter: Ritter
        },
        manufacturer_constants.INTERTECHNO: {
            manufacturer_constants.CMR_300: CMR300,
            manufacturer_constants.CMR_500: CMR500,
            manufacturer_constants.CMR_1000: CMR1000,
            manufacturer_constants.CMR_1224: CMR1224,
            manufacturer_constants.GRR_300: GRR300,
            manufacturer_constants.ITR_300: ITR300,
            manufacturer_constants.ITR_3500: ITR3500,
            manufacturer_constants.PA3_1000: PA31000,
            manufacturer_constants.PAR_1500: PAR1500,
            manufacturer_constants.YCR_1000: YCR1000
        }
    }

    _broadcast_message = "SEARCH HCGW"

    def __init__(self, host: str = None, port: int = 49880):
        """
        Creates a new client object.

        :param host: host address of the RaspyRFM module
        :param port: the port on which the RaspyRFM module is listening
        """

        self._host = host
        self._port = port

        self._manufacturer = None
        self._model = None
        self._firmware_version = None

    def search(self) -> str:
        """
        Sends a local network broadcast with a specified message.
        If a gateway is present it will respond to this broadcast.

        If a valid response is found the properties of this client object will be updated accordingly.

        :return: ip of the detected gateway
        """
        cs = socket.socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        cs.sendto(bytes(self._broadcast_message, "utf-8"), ('255.255.255.255', 49880))

        cs.setblocking(True)
        cs.settimeout(1)

        try:
            data, address = cs.recvfrom(4096)
            print("Received message: \"%s\"", data)
        except socket.timeout:
            print("Timeout")
            return None

        message = data.decode('utf-8')

        # abort if response is invalid
        if not message.startswith('HCGW:'):
            print("Invalid response")
            return None

        # RaspyRFM response:
        # "HCGW:VC:Seegel Systeme;MC:RaspyRFM;FW:1.00;IP:192.168.2.124;;"

        # try to parse data if valid
        self._manufacturer = message[message.index('VC:'):message.index(';MC')]
        self._model = message[message.index('MC:'):message.index(';FW')]
        self._firmware_version = message[message.index('FW:'):message.index(';IP')]
        parsed_host = message[message.index('IP:'):message.index(';;')]
        if self._host is None:
            self._host = parsed_host

        return parsed_host

    def get_manufacturer(self) -> str:
        """
        :return: the manufacturer description
        """
        return self._manufacturer

    def get_model(self) -> str:
        """
        :return: the model description
        """
        return self._model

    def get_host(self) -> str:
        """
        :return: the ip/host address of the gateway (if one was found or specified manually)
        """
        return self._host

    def get_port(self) -> int:
        """
        :return: the port of the gateway
        """
        return self._port

    def get_firmware_version(self) -> str:
        """
        :return: the gateway firmware version
        """
        return self._firmware_version

    def get_device(self, manufacturer: str, model: str) -> Device:
        return self.__manufacturer_model_dict[manufacturer][model]()

    def list_supported_devices(self):
        import pprint
        pprint.pprint(self.__manufacturer_model_dict)

    def send(self, device: Device, action: str) -> None:
        """
        Use this method to generate codes for actions on supported devices.
        It will generates a string that can be interpreted by the the RaspyRFM module.
        The string contains information about the rc signal that should be sent.

        :param device: the device
        :param action: action to execute
        """

        if self._host is None:
            print("Missing host, nothing sent.")
            return

        message = device.generate_code(action)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(bytes(message, "utf-8"), (self._host, self._port))
