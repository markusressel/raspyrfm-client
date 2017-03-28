from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.universal.HX2262Compatible import HX2262Compatible


class ZtcS316A(HX2262Compatible):
    _h = '0'
    _l = 'f'
    _on = ['0', '1']
    _off = ['1', '0']
    _repetitions = 5

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.WESTFALIA, manufacturer_constants.ZTC_S316A)

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]

    def get_channel_config_args(self):
        return {
            'A': '^[01]$',
            'B': '^[01]$',
            'C': '^[01]$',
            'D': '^[01]$',
            'E': '^[01]$',
            'F': '^[01]$',
            'CH': '^[1-4]$'
        }

    def get_bit_data(self, action: str):
        cfg = self.get_channel_config()
        bits = []

        for i in range(6):
            bits += self._h if cfg[chr(i + ord('A'))] == '1' else self._l

        for i in range(4):
            bits += self._h if int(cfg['CH']) == (4 - i) else self._l

        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off

        return bits, self._repetitions
