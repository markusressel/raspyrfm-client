"""
Base class for all device implementations
"""


class Device(object):
    def __init__(self, manufacturer: str, model: str, connairparams: {} = None):
        self._manufacturer = manufacturer
        self._model = model
        self._channel = None
        self._connair_params = connairparams

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
        
    def get_channel_config(self) -> dict or None:
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
        
    def generate_conair_code(self, data: []) -> None:
        if self._connair_params is None:
            raise ValueError("connair parameters not set")
        if 'repetitions' not in self._connair_params:
            raise ValueError("connair repetitions missing")
        if 'pauselen' not in self._connair_params:
            raise ValueError("connair pauselen missing")
        if 'steplen' not in self._connair_params:
            raise ValueError("connair steplen missing")
        _head_connair = "TXP:0,0,"
        _code = _head_connair
        _code = _code + str(self._connair_params['repetitions']) + ','
        _code = _code + str(self._connair_params['pauselen']) + ','
        _code = _code + str(self._connair_params['steplen']) + ','
        _code = _code + str(len(data)) + ','
        for pulse in data:
            _code = _code + str(pulse[0]) + ','
            _code = _code + str(pulse[1]) + ','
        return _code[:-1]