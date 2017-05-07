"""
Example usage of the RaspyRFMClient can be found in the example.py file
"""
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import Device
from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
from raspyrfm_client.device_implementations.gateway.base import Gateway
from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer


class RaspyRFMClient:
    """
    This class is the main interface for generating and sending signals.
    """

    """
    This dictionary maps manufacturer and model constants to their implementation class.
    It is filled automatically when creating an instance of this class.
    """
    _GATEWAY_IMPLEMENTATIONS_DICT = {}
    _CONTROLUNIT_IMPLEMENTATIONS_DICT = {}

    _broadcast_message = b'SEARCH HCGW'

    def __init__(self):
        """
        Creates a new client object.
        """
        self.reload_implementation_classes()

    def reload_implementation_classes(self):
        """
        Dynamically reloads device implementations 
        """
        print("Loading implementation classes...")
        self._reload_gateway_implementations()
        self._reload_controlunit_implementations()
        print("Done!")

    @staticmethod
    def __import_submodules(package, recursive=True):
        """ Import all submodules of a module, recursively, including subpackages

        :param package: package (name or actual module)
        :param recursive: loads all subpackages
        :type package: str | module
        :rtype: dict[str, types.ModuleType]
        """
        import pkgutil
        import importlib

        if isinstance(package, str):
            package = importlib.import_module(package)
        results = {}
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                results.update(RaspyRFMClient.__import_submodules(full_name))
        return results

    @staticmethod
    def __get_all_subclasses(base_class):
        """
        Returns a list of all currently imported classes that are subclasses (even multiple levels)
        of the specified base class.
        :param base_class: base class to match classes to
        :return: list of classes
        """
        all_subclasses = []

        for subclass in base_class.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(RaspyRFMClient.__get_all_subclasses(subclass))

        return all_subclasses

    def _reload_gateway_implementations(self) -> None:
        """
        Finds gateway implementations in the "raspyrfm_client.device_implementations.gateway.manufacturer" package.
        This works by recursively searching through supbackages and finding classes that have
        the gateway base class (base.py) as a superclass.
        """
        self._GATEWAY_IMPLEMENTATIONS_DICT = {}

        from raspyrfm_client.device_implementations.gateway import manufacturer
        RaspyRFMClient.__import_submodules(manufacturer)

        for gateway_implementation in RaspyRFMClient.__get_all_subclasses(Gateway):
            gateway_instance = gateway_implementation()
            brand = gateway_instance.get_manufacturer()
            model = gateway_instance.get_model()

            # ignore classes that are disabled by the developer
            if hasattr(gateway_instance, "DISABLED") and gateway_instance.DISABLED is True:
                continue

            if brand not in self._GATEWAY_IMPLEMENTATIONS_DICT:
                self._GATEWAY_IMPLEMENTATIONS_DICT[brand] = {}

            self._GATEWAY_IMPLEMENTATIONS_DICT[brand][model] = gateway_implementation

    def _reload_controlunit_implementations(self) -> None:
        """
        Finds device implementations in the "raspyrfm_client.device_implementations.manufacturer" package.
        This works by recursively searching through supbackages and finding classes that have
        the device base class (base.py) as a superclass.
        """

        self._CONTROLUNIT_IMPLEMENTATIONS_DICT = {}

        from raspyrfm_client.device_implementations.controlunit import manufacturer
        RaspyRFMClient.__import_submodules(manufacturer)

        for device_implementation in RaspyRFMClient.__get_all_subclasses(Device):
            device_instance = device_implementation()
            brand = device_instance.get_manufacturer()
            model = device_instance.get_model()

            # ignore classes that are disabled by the developer
            if hasattr(device_instance, "DISABLED") and device_instance.DISABLED is True:
                continue

            if brand not in self._CONTROLUNIT_IMPLEMENTATIONS_DICT:
                self._CONTROLUNIT_IMPLEMENTATIONS_DICT[brand] = {}

            self._CONTROLUNIT_IMPLEMENTATIONS_DICT[brand][model] = device_implementation

    def search(self) -> str or None:
        """
        Sends a local network broadcast with a specified message.
        If a gateway is present it will respond to this broadcast.

        If a valid response is found the properties of this client object will be updated accordingly.

        :return: ip of the detected gateway
        """
        cs = socket.socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        cs.sendto(self._broadcast_message, ('255.255.255.255', 49880))

        cs.setblocking(True)
        cs.settimeout(1)

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
            _manufacturer = message[message.index('VC:') + 3:message.index(';MC')]
            _model = message[message.index('MC:') + 3:message.index(';FW')]
            _firmware_version = message[message.index('FW:') + 3:message.index(';IP')]
            parsed_host = message[message.index('IP:') + 3:message.index(';;')]

            if self._host is None:
                if parsed_host != address[0]:
                    self._host = address[0]
                else:
                    self._host = parsed_host

            return parsed_host

        except socket.timeout:
            return None

    def get_gateway(self, manufacturer: Manufacturer, model: GatewayModel, host: str = None,
                    port: int = None) -> Gateway:
        """
        Use this method to get a gateway implementation intance
        :param manufacturer: gateway manufacturer
        :param model: gateway model
        :param host: gateway host address (optional)
        :param port: gateway port (optional)
        :return: gateway implementation
        """
        return self._GATEWAY_IMPLEMENTATIONS_DICT[manufacturer][model](host, port)

    def get_device(self, manufacturer: Manufacturer, model: ControlUnitModel) -> Device:
        """
        Use this method to get a device implementation intance
        :param manufacturer: device manufacturer
        :param model: device model
        :return: device implementation
        """
        return self._CONTROLUNIT_IMPLEMENTATIONS_DICT[manufacturer][model]()

    def get_supported_manufacturers(self) -> [str]:
        """
        :return: a list of supported manufacturer names
        """
        return self._CONTROLUNIT_IMPLEMENTATIONS_DICT.keys()

    def get_supported_models(self, manufacturer: Manufacturer) -> [ControlUnitModel]:
        """
        :param manufacturer: supported manufacturer name
        :return: a list of supported model names for this manufacturer
        """
        return self._CONTROLUNIT_IMPLEMENTATIONS_DICT[manufacturer].keys()

    def list_supported_gateways(self) -> None:
        """
        Prints an indented list of all supported manufacturers and models
        """
        for manufacturer in self._GATEWAY_IMPLEMENTATIONS_DICT:
            print(manufacturer.value)
            for model in self._GATEWAY_IMPLEMENTATIONS_DICT[manufacturer].keys():
                print("  " + model.value)

    def list_supported_controlunits(self) -> None:
        """
        Prints an indented list of all supported manufacturers and models
        """
        for manufacturer in self._CONTROLUNIT_IMPLEMENTATIONS_DICT:
            print(manufacturer.value)
            for model in self._CONTROLUNIT_IMPLEMENTATIONS_DICT[manufacturer].keys():
                print("  " + model.value)

    def send(self, gateway: Gateway, device: Device, action: Action) -> None:
        """
        Use this method to generate codes for actions on supported device.
        It will generates a string that can be interpreted by the the RaspyRFM module.
        The string contains information about the rc signal that should be sent.

        :param gateway: the gateway to generate the code for
        :param device: the device to generate the code for
        :param action: action to execute
        """

        if gateway.get_host() is None:
            print("Missing host, nothing sent.")
            return

        message = gateway.generate_code(device, action)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(bytes(message, "utf-8"), (gateway.get_host(), gateway.get_port()))
