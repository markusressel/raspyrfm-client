from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device


class CMR1000(Device):
    _lo = "4,"
    _hi = "12,"
    _seqHi = _hi + _lo + _hi + _lo
    _seqLo = _lo + _hi + _lo + _hi
    _seqFl = _lo + _hi + _hi + _lo
    _h = _seqFl
    _l = _seqLo
    _on = _seqFl + _seqFl
    _off = _seqFl + _seqLo
    _additional = _seqLo + _seqFl

    _tx433version = "1,"

    _s_speed_connair = "140"
    _head_connair = "TXP:0,0,6,11125,89,25,"
    _tail_connair = _tx433version + _s_speed_connair + ";"

    _s_speed_itgw = "125,"
    _head_itgw = "0,0,6,11125,89,26,0,"
    _tail_itgw = _tx433version + _s_speed_itgw + "0"

    _master_dict = {
        "A": _l + _l + _l + _l,
        "B": _h + _l + _l + _l,
        "C": _l + _h + _l + _l,
        "D": _h + _h + _l + _l,
        'E': _l + _l + _h + _l,
        'F': _h + _l + _h + _l,
        'G': _l + _h + _h + _l,
        'H': _h + _h + _h + _l,
        'I': _l + _l + _l + _h,
        'J': _h + _l + _l + _h,
        'K': _l + _h + _l + _h,
        'L': _h + _h + _l + _h,
        'M': _l + _l + _h + _h,
        'N': _h + _l + _h + _h,
        'O': _l + _h + _h + _h,
        'P': _h + _h + _h + _h
    }

    _slave_dict = {
        1: _l + _l + _l + _l,
        2: _h + _l + _l + _l,
        3: _l + _h + _l + _l,
        4: _h + _h + _l + _l,
        5: _l + _l + _h + _l,
        6: _h + _l + _h + _l,
        7: _l + _h + _h + _l,
        8: _h + _h + _h + _l,
        9: _l + _l + _l + _h,
        10: _h + _l + _l + _h,
        11: _l + _h + _l + _h,
        12: _h + _h + _l + _h,
        13: _l + _l + _h + _h,
        14: _h + _l + _h + _h,
        15: _l + _h + _h + _h,
        16: _h + _h + _h + _h
    }

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(CMR1000, self).__init__(manufacturer_constants.INTERTECHNO, manufacturer_constants.CMR_1000)

    def setup_channel(self, **channel_arguments) -> None:
        """
        :param channel_arguments: master='A', slave=1
        """
        if channel_arguments["master"] not in self._master_dict:
            raise ValueError("Invalid Master")

        if channel_arguments["slave"] not in self._slave_dict:
            raise ValueError("Invalid Slave")

        self._channel = channel_arguments

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]

    def generate_code(self, action: str) -> str:
        if self.get_channel() is None:
            raise ValueError("Missing channel configuration :(")

        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)

        if action is actions.ON:
            return self._head_connair + self._master_dict[self.get_channel()["master"]] + self._slave_dict[
                self.get_channel()["slave"]] + self._additional + self._on + self._tail_connair
        elif action is actions.OFF:
            return self._head_connair + self._master_dict[self.get_channel()["master"]] + self._slave_dict[
                self.get_channel()["slave"]] + self._additional + self._off + self._tail_connair
        else:
            raise ValueError("Invalid action")
