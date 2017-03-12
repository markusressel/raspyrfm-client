from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device


class AB440S(Device):
    _lo = "1,"
    _hi = "3,"
    _seqLo = _lo + _hi + _lo + _hi
    _seqHi = _hi + _lo + _hi + _lo
    _seqFl = _lo + _hi + _hi + _lo
    _on = _seqLo + _seqFl
    _off = _seqFl + _seqLo

    _tx433version = "1,"

    _s_speed_connair = "14"
    _head_connair = "TXP:0,0,10,5600,350,25,"
    _tail_connair = _tx433version + _s_speed_connair + ";"

    _s_speed_itgw = "32,"
    _head_itgw = "0,0,10,11200,350,26,0,"
    _tail_itgw = _tx433version + _s_speed_itgw + "0"

    _dips = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.ELRO, manufacturer_constants.AB440S)

    def setup_channel(self, **channel_arguments) -> None:
        """
        :param channel_arguments: dips=[boolean]
        """
        for dip in self._dips:
            if dip not in channel_arguments:
                raise ValueError("arguments should contain key \"" + str(dip) + "\"")

        self._channel = channel_arguments

    def get_channel(self) -> dict:
        return self._channel

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]

    def generate_code(self, action: str) -> str:
        dips = self.get_channel()
        if dips is None:
            raise ValueError("Missing channel configuration :(")

        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)

        seq = ""

        for dip in self._dips:
            dip_is_on = self.get_channel()[dip]
            if dip_is_on:
                seq += self._seqLo
            else:
                seq += self._seqFl

        if action is actions.ON:
            return self._head_connair + seq + self._on + self._tail_connair
        elif action is actions.OFF:
            return self._head_connair + seq + self._off + self._tail_connair
        else:
            raise ValueError("Invalid action")
