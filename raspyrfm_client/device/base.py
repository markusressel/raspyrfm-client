"""
Base class for all device implementations
"""

import re


class Device(object):
    """
    regular expression check for channel config
    _argchecks example:
    _argschecks = {"ID": "^[A-F]$", "CH": "^[1-4]$"}
    """
    _argchecks = {}

    _connair_params = {}
    
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
        
    def check_channel_config(self, **channel_arguments):
        """
        :return: boolean if check is ok, see documentation for member _argchecks
        """
        for arg in self._argchecks:
            if arg not in channel_arguments:
                raise ValueError("arguments should contain key \"" + arg + "\"")
            if re.match(self._argchecks[arg], str(channel_arguments[arg])) is None:
                raise ValueError("argument \"" + arg + "\" out of range, does not match to " + self._argchecks[arg])
                
        self._channel = channel_arguments

    def set_channel_config(self, **channel_arguments) -> None:
        """
        Sets the channel as multiple arguments.
        See implementation specific details about how the channel should be passed in.

        :param channel_arguments:
        """
        if self.check_channel_config(**channel_arguments):
            self._channel = channel_arguments
        
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
        This method can be implemented by inheriting classes if it does not implement get_pulse_data
        :param action: action to execute
        :return: signal code
        """
        if self.get_channel_config() is None:
            raise ValueError("Missing channel configuration :(")
        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)
            
        if self._connair_params is None:
            raise ValueError("connair parameters not set")
        if 'repetitions' not in self._connair_params:
            raise ValueError("connair repetitions missing")
        if 'pauselen' not in self._connair_params:
            raise ValueError("connair pauselen missing")
        if 'steplen' not in self._connair_params:
            raise ValueError("connair steplen missing")
        
        pulsedata = self.get_pulse_data(action)
        _head_connair = "TXP:0,0,"
        _code = _head_connair
        _code = _code + str(self._connair_params['repetitions']) + ','
        _code = _code + str(self._connair_params['pauselen']) + ','
        _code = _code + str(self._connair_params['steplen']) + ','
        
        _code = _code + str(len(pulsedata)) + ','
        for pulse in pulsedata:
            _code = _code + str(pulse[0]) + ','
            _code = _code + str(pulse[1]) + ','
        return _code[:-1]