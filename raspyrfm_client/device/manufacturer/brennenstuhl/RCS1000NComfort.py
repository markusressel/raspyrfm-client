from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class RCS1000NComfort(HX2262Compatible):
    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.BRENNENSTUHL,
                         manufacturer_constants.RCS_1000_N_COMFORT)

    def set_channel_config(self, **channel_arguments) -> None:
        """
        :param channel_arguments: 1=False, 2=False, ... , 5=False, A=True, B=False, ... , E=False
        """
        for dip in self._dips:
            if dip not in channel_arguments:
                raise ValueError("arguments should contain key \"" + str(dip) + "\"")

        self._channel = channel_arguments

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]

    def generate_code(self, action: str) -> str:
        cfg = self.get_channel_config()
        if cfg is None:
            raise ValueError("Missing channel configuration :(")
        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)
            
        bits = []
        
        for i in range(5):
            bits.append('0' if cfg[chr(i + ord('1'))] else 'f')
            
        for i in range(5):
            bits.append('0' if cfg[chr(i + ord('A'))]  else 'f')
            
        if action is actions.ON:
            bits += ['f', 'f']
        elif action is actions.OFF:
            bits += ['f', '0']
        else:
            raise ValueError("Invalid action")
            
        super().set_bits(bits)
            
        return super().generate_code()