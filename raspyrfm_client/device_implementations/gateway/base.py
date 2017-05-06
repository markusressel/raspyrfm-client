from raspyrfm_client.device_implementations.controlunit.base import Device


class Gateway(object):
    """
    Base gateway implementation
    """

    def __init__(self, manufacturer: str, model: str):
        self._model = model

    def get_manufacturer(self) -> str:
        """
        :return: the device_implementations manufacturer
        """
        return self._manufacturer

    def get_model(self) -> str:
        """
        :return: the device_implementations model
        """
        return self._model

    def generate_code(self, device: Device, action: str) -> str:
        raise NotImplementedError
