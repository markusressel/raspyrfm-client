"""
Base class for all device implementations
"""

import re


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
        argchecks = self.get_channel_config_args()
        for arg in argchecks:
            if arg not in channel_arguments:
                raise ValueError("arguments should contain key \"" + arg + "\"")
            if re.match(argchecks[arg], str(channel_arguments[arg])) is None:
                raise ValueError("argument \"" + arg + "\" out of range, does not match to " + argchecks[arg])

        self._channel = channel_arguments

    def get_channel_config_args(self):
        """
        gets required config arguments and their regular expression to check the erguments
        has to be implemented by inheriting classes
        
        :return: dictionary of arguments
        
        example: {"ID": "^[A-F]$", "CH": "^[1-4]$"}
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

    def get_pulse_data(self):
        """
        generates pulse data
        :return: (pulse pairs, repetitions, timebase)
        """
        raise NotImplementedError

    # obsolete as soon as a different layer generations code from pulse_data
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

        pulsedata = self.get_pulse_data(action)
        _head_connair = "TXP:0,0,"
        _code = _head_connair
        _code = _code + str(pulsedata[1]) + ','  # add repetitions
        _code = _code + str(5600) + ','
        _code = _code + str(pulsedata[2]) + ','  # add timebase

        _code = _code + str(len(pulsedata[0])) + ','
        for pulse in pulsedata[0]:
            _code = _code + str(pulse[0]) + ','
            _code = _code + str(pulse[1]) + ','
        return _code[:-1]
