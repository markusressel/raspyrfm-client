from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import ControlUnit
from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer


class Gateway(object):
    """
    Base gateway implementation
    """

    def __init__(self, manufacturer: Manufacturer, model: GatewayModel, host: str, port: int):
        self._manufacturer = manufacturer
        self._model = model
        self._firmware_version = None

        if host is None:
            host = "127.0.0.1"
        self._host = host

        if port is None:
            port = 49880
        self._port = port

    def get_manufacturer(self) -> Manufacturer:
        """
        :return: the gateway manufacturer
        """
        return self._manufacturer

    def get_model(self) -> GatewayModel:
        """
        :return: the gateway model
        """
        return self._model

    def get_firmware_version(self) -> str:
        """
        :return: the gateway firmware version
        """
        return self._firmware_version

    def get_host(self) -> str:
        """
        :return: the ip/host address of the gateway (if one was found or specified manually)
        """
        return self._host

    def get_port(self) -> int:
        """
        :return: port of the gateway 
        """
        return self._port

    def get_search_response_regex_literal(self) -> str:
        """
        :return: a regular expression that matches the response to a "search" broadcast 
        """
        raise NotImplementedError

    @staticmethod
    def create_from_broadcast(host: str, message: str):
        """
        :param host: the host that sent the message
        :param message: the search response message
        :return: a new instance of this gateway based on a broadcast response message
        """
        raise NotImplementedError

    def generate_code(self, device: ControlUnit, action: Action) -> str:
        raise NotImplementedError
