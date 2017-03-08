from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device


class Telecontrol(Device):
    _lo = "1,"
    _hi = "3,"
    _seqHi = _hi + _lo + _hi + _lo
    _seqLo = _lo + _hi + _lo + _hi
    _seqFl = _lo + _hi + _hi + _lo
    _h = _seqFl
    _l = _seqHi
    _on = _seqFl + _seqFl
    _off = _seqLo + _seqLo
    _additional = _seqLo + _seqFl + _seqFl

    _tx433version = "1,"

    _s_speed_connair = "16"
    _head_connair = "TXP:0,0,10,5600,350,25,"
    _tail_connair = _tx433version + _s_speed_connair + ";"

    _s_speed_itgw = "32,"
    _head_itgw = "0,0,10,11200,350,26,0,"
    _tail_itgw = _tx433version + _s_speed_itgw + "0"

    _master_dict = {
        "A": _l + _h + _h + _h,
        "B": _h + _l + _h + _h,
        "C": _h + _h + _l + _h,
        "D": _h + _h + _h + _l
    }

    _slave_dict = {
        1: _l + _h + _h,
        2: _h + _l + _h,
        3: _h + _h + _l
    }

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(Telecontrol, self).__init__(manufacturer_constants.REV, manufacturer_constants.Telecontrol)

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
