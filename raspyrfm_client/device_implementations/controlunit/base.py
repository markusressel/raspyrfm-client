"""
Base class for all controlunit implementations
"""

import re

from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer


class ControlUnit(object):
    def __init__(self, manufacturer: Manufacturer, model: ControlUnitModel):
        self._manufacturer = manufacturer
        self._model = model
        self._channel = None

    def __str__(self):
        return ("Manufacturer: " + self._manufacturer.value + "\n" +
                "Model: " + self._model.value + "\n" +
                "Supported Actions: " + str(self.get_supported_actions()) + "\n" +
                "Channel: " + str(self.get_channel_config()))

    def get_manufacturer(self) -> Manufacturer:
        """
        :return: the device manufacturer
        """
        return self._manufacturer

    def get_model(self) -> ControlUnitModel:
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

    def get_supported_actions(self) -> [Action]:
        """
        :return: the supported actions of this device
        """
        raise NotImplementedError

    def get_pulse_data(self, action: Action):
        """
        generates pulse data
        :return: (pulse pairs, repetitions, timebase)
        """
        raise NotImplementedError
