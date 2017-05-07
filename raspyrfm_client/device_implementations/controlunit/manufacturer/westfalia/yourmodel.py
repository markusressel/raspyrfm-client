from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import ControlUnit


class YourModel(ControlUnit):
    def __init__(self):
        from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
        from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel
        super().__init__(Manufacturer.YourManufacturer, ControlUnitModel.YourModel)

    def get_channel_config_args(self):
        return {}

    def get_pulse_data(self, action: Action):
        return [[0, 0], [0, 0]], 0, 0

    def get_supported_actions(self) -> [str]:
        return [Action.ON]
