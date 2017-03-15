"""
Base class for all device implementations
"""


class Device(object):
    def __init__(self, manufacturer: str, model: str):
        self._manufacturer = manufacturer
        self._model = model
        self._channel = None

    def __str__(self):
        return ("Manufacturer: " + self._manufacturer + "\n" +
                "Model: " + self._model + "\n" +
                "Supported Actions: " + str(self.get_supported_actions()) + "\n" +
                "Channel: " + str(self.get_channel_config()))

    def get_manufacturer(self) -> str:
        """
        :return: the device manufacturer
        """
        return self._manufacturer

    def get_model(self) -> str:
        """
        :return: the device model
        """
        return self._model

    def set_channel_config(self, **channel_arguments) -> None:
        """
        Sets the channel as multiple arguments.
        See implementation specific details about how the channel should be passed in.

        :param channel_arguments:
        """
        raise NotImplementedError

    def get_channel_config(self) -> dict:
        """
        :return: the channel setup as a dict
        """
        return self._channel

    def get_supported_actions(self) -> [str]:
        """
        :return: the supported actions of this device
        """
        raise NotImplementedError

    def generate_code(self, action: str) -> str:
        """
        This method should be implemented by inheriting classes

        :param action: action to execute
        :return: signal code
        """
        raise NotImplementedError
