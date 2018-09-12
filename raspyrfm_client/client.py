"""
Example usage of the RaspyRFMClient can be found in the example.py file
"""
import socket

from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import ControlUnit
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
            # ignore classes that are disabled by the developer
            if hasattr(gateway_implementation, "DISABLED") and gateway_implementation.DISABLED is True:
                continue

            gateway_instance = gateway_implementation()
            brand = gateway_instance.get_manufacturer()
            model = gateway_instance.get_model()

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

        for device_implementation in RaspyRFMClient.__get_all_subclasses(ControlUnit):
            # ignore classes that are disabled by the developer
            if hasattr(device_implementation, "DISABLED") and device_implementation.DISABLED is True:
                continue

            device_instance = device_implementation()
            brand = device_instance.get_manufacturer()
            model = device_instance.get_model()

            if brand not in self._CONTROLUNIT_IMPLEMENTATIONS_DICT:
                self._CONTROLUNIT_IMPLEMENTATIONS_DICT[brand] = {}

            self._CONTROLUNIT_IMPLEMENTATIONS_DICT[brand][model] = device_implementation

    def get_supported_gateway_manufacturers(self):
        """
        :return: a list of supported gateway manufacturers
        """
        return self._GATEWAY_IMPLEMENTATIONS_DICT.keys()

    def get_supported_gateway_models(self, manufacturer: Manufacturer) -> [GatewayModel]:
        """
        :param manufacturer: supported gateway manufacturer
        :return: a list of supported gateway models for this gateway manufacturer
        """
        return self._GATEWAY_IMPLEMENTATIONS_DICT[manufacturer].keys()

    def get_gateway(self, manufacturer: Manufacturer, model: GatewayModel, host: str = None,
                    port: int = None) -> Gateway:
        """
        Use this method to get a gateway implementation instance
        :param manufacturer: gateway manufacturer
        :param model: gateway model
        :param host: gateway host address (optional)
        :param port: gateway port (optional)
        :return: gateway implementation
        """
        return self._GATEWAY_IMPLEMENTATIONS_DICT[manufacturer][model](host, port)

    def get_supported_controlunit_manufacturers(self) -> [str]:
        """
        :return: a list of supported control unit manufacturers
        """
        return self._CONTROLUNIT_IMPLEMENTATIONS_DICT.keys()

    def get_supported_controlunit_models(self, manufacturer: Manufacturer) -> [ControlUnitModel]:
        """
        :param manufacturer: supported control unit manufacturer
        :return: a list of supported control unit models for this manufacturer
        """
        return self._CONTROLUNIT_IMPLEMENTATIONS_DICT[manufacturer].keys()

    def get_controlunit(self, manufacturer: Manufacturer, model: ControlUnitModel) -> ControlUnit:
        """
        Use this method to get a device implementation intance
        :param manufacturer: device manufacturer
        :param model: device model
        :return: device implementation
        """
        return self._CONTROLUNIT_IMPLEMENTATIONS_DICT[manufacturer][model]()

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

    def search(self) -> [Gateway]:
        """
        Sends a local network broadcast with a specified message.
        If a gateway is present it will respond to this broadcast.

        If a valid response is found the properties of this client object will be updated accordingly.

        :return: list of gateways
        """

        import re
        import socket
        from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

        found_gateways = []
        all_gateways = []

        # get all gateway implementations in a list
        for manufacturer in self.get_supported_gateway_manufacturers():
            for model in self.get_supported_gateway_models(manufacturer):
                all_gateways.append(self.get_gateway(manufacturer, model))

        # send the broadcast
        cs = socket.socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        _broadcast_message = b'SEARCH HCGW'

        cs.sendto(_broadcast_message, ('255.255.255.255', 49880))

        cs.setblocking(True)
        cs.settimeout(1)

        # receive the message(s)
        try:
            while True:
                data, address = cs.recvfrom(4096)
                # print("Received message: \"%s\"" % data)
                # print("Address: " + address[0])

                message = data.decode()

                # for each device implementation, check if the response matches the expected pattern
                # and add an instance of this gateway implementation to the found_gateways list
                for gateway in all_gateways:
                    if re.match(gateway.get_search_response_regex_literal(), message) is not None:
                        found_gateways.append(gateway.create_from_broadcast(address[0], message))

        except socket.timeout:
            return found_gateways
        finally:
            return found_gateways

    def send(self, gateway: Gateway, device: ControlUnit, action: Action) -> None:
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

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # UDP
            sock.sendto(bytes(message, "utf-8"), (gateway.get_host(), gateway.get_port()))
