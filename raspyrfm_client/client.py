"""
TODO:

Example usage can be found in the example.py file
"""
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

from raspyrfm_client.device.base import Device
from raspyrfm_client.device.manufacturer import manufacturer_constants
from raspyrfm_client.device.manufacturer.BAT.RC3500_A_IP44_DE import RC3500_A_IP44_DE
from raspyrfm_client.device.manufacturer.BAT.RC_AAA1000_A_IP44_Outdoor import RC_AAA1000_A_IP44_Outdoor
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
from raspyrfm_client.device.manufacturer.brennenstuhl.RCS1000NComfort import RCS1000NComfort
from raspyrfm_client.device.manufacturer.brennenstuhl.RCS1044NComfort import RCS1044NComfort
from raspyrfm_client.device.manufacturer.elro.AB440D_200W import AB440D_200W
from raspyrfm_client.device.manufacturer.elro.AB440ID import AB440ID
from raspyrfm_client.device.manufacturer.elro.AB440L import AB440L
from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S
from raspyrfm_client.device.manufacturer.elro.AB440SC import AB440SC
from raspyrfm_client.device.manufacturer.elro.AB440WD import AB440WD
from raspyrfm_client.device.manufacturer.intertek.Model1919361 import Model1919361
from raspyrfm_client.device.manufacturer.mumbi.MFS300 import MFS300
from raspyrfm_client.device.manufacturer.pollin_electronic.Set2605 import Set2605


class RaspyRFMClient:
    """
    This class is the main interface for generating and sending signals.
    """

    """
    This dictionary maps manufacturer and model constants to their implementation class

    TODO: find implementations dynamically (if possible)
    """
    __manufacturer_model_dict = {
        manufacturer_constants.BAT: {
            manufacturer_constants.RC3500_A_IP44_DE: RC3500_A_IP44_DE,
            manufacturer_constants.RC_AAA1000_A_IP44_Outdoor: RC_AAA1000_A_IP44_Outdoor
        },
        manufacturer_constants.BRENNENSTUHL: {
            manufacturer_constants.RCS_1000_N_COMFORT: RCS1000NComfort,
            manufacturer_constants.RCS_1044_N_COMFORT: RCS1044NComfort
        },
        manufacturer_constants.ELRO: {
            manufacturer_constants.AB440D_200W: AB440D_200W,
            manufacturer_constants.AB440ID: AB440ID,
            manufacturer_constants.AB440L: AB440L,
            manufacturer_constants.AB440S: AB440S,
            manufacturer_constants.AB440SC: AB440SC,
            manufacturer_constants.AB440WD: AB440WD
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
        },
        manufacturer_constants.INTERTEK: {
            manufacturer_constants.MODEL_1919361: Model1919361
        },
        manufacturer_constants.MUMBI: {
            manufacturer_constants.M_FS300: MFS300
        },
        manufacturer_constants.POLLIN_ELECTRONIC: {
            manufacturer_constants.SET_2605: Set2605
        },
        manufacturer_constants.REV: {
            manufacturer_constants.Telecontrol: Telecontrol,
            manufacturer_constants.Ritter: Ritter
        },
    }

    _broadcast_message = b'SEARCH HCGW'

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

        cs.sendto(self._broadcast_message, ('255.255.255.255', self._port))

        cs.setblocking(True)
        cs.settimeout(1)

        data = None
        try:
            data, address = cs.recvfrom(4096)
            print("Received message: \"%s\"" % data)
            print("Address: " + address[0])

            message = data.decode()

            # abort if response is invalid
            if not message.startswith('HCGW:'):
                print("Invalid response")
                return None

            # RaspyRFM response:
            # "HCGW:VC:Seegel Systeme;MC:RaspyRFM;FW:1.00;IP:192.168.2.124;;"

            # try to parse data if valid
            self._manufacturer = message[message.index('VC:') + 3:message.index(';MC')]
            self._model = message[message.index('MC:') + 3:message.index(';FW')]
            self._firmware_version = message[message.index('FW:') + 3:message.index(';IP')]
            parsed_host = message[message.index('IP:') + 3:message.index(';;')]

            if self._host is None:
                if parsed_host != address[0]:
                    self._host = address[0]
                else:
                    self._host = parsed_host

            return parsed_host

        except socket.timeout:
            print("Timeout")
            print("Data: " + str(data))
            return None

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
