from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import Device
from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer


class Gateway(object):
    """
    Base gateway implementation
    """

    def __init__(self, manufacturer: Manufacturer, model: GatewayModel):
        self._manufacturer = manufacturer
        self._model = model

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

    def generate_code(self, device: Device, action: Action) -> str:
        raise NotImplementedError
