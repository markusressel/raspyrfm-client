from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device


class HX2262Compatible(Device):
    _lo = "1,"
    _hi = "3,"
    _seqLo = _lo + _hi + _lo + _hi
    _seqHi = _hi + _lo + _hi + _lo
    _seqFl = _lo + _hi + _hi + _lo

    _head_connair = "TXP:0,0,10,5600,350,25,"
    
    _sync_high = "1,"
    _sync_low = "31"
    _tail_connair = _sync_high + _sync_low + ";"

    
    _dips = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    from raspyrfm_client.device.manufacturer import manufacturer_constants
    def __init__(self, manufacturer: str = manufacturer_constants.UNIVERSAL, model: str = manufacturer_constants.HX2262):
        super().__init__(manufacturer, model)

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

    def generate_code(self, action: str = None) -> str:
        dips = self.get_channel_config()
        if dips is None:
            raise ValueError("Missing channel configuration :(")

        seq = ""
        
        for dip in self._dips:
            dip_value = str(self.get_channel_config()[dip]).lower()
            if dip_value.lower() == 'f':
                seq += self._seqFl
            elif dip_value.lower() == '0':
                seq += self._seqLo
            elif dip_value.lower() == '1':
                seq += self._seqHi
            else:
                raise ValueError(
                    "Invalid dip value \"" + dip_value + "\"! Must be one of ['0', '1', 'f'] (case insensitive)")

        return self._head_connair + seq + self._tail_connair
