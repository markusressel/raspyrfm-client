from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class ZtcS316A(HX2262Compatible):
    _on = ['0', '1']
    _off = ['1', '0']
    _dips = ['A', 'B', 'C', 'D', 'E', 'F', '4', '3', '2', '1']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.WESTFALIA, manufacturer_constants.ZTC_S316A)

    def set_channel_config(self, **channel_arguments) -> None:
        """
        :param channel_arguments: dips=[boolean]
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
        
        for dip in self._dips:
            print("Setting DIP", dip)
            dip_is_on = self.get_channel_config()[dip]
            if dip_is_on:
                bits += ['0']
            else:
                bits += ['f']
        
        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        super().set_bits(bits)
            
        return super().generate_code()