from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S


class AB440ID(AB440S):
    _s_speed_itgw = "125,"

    _dips = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.ELRO,
                                     manufacturer_constants.AB440ID)

    def generate_code(self, action: str) -> str:
        dips = self.get_channel()
        if dips is None:
            raise ValueError("Missing channel configuration :(")

        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)

        seq = ""

        for i, dip in enumerate(self._dips):
            if i < 5:
                continue
            else:
                dip_is_on = self.get_channel()[dip]
                if dip_is_on:
                    seq += self._seqLo
                else:
                    seq += self._seqFl

        # middle part
        seq += self._seqFl + self._seqFl

        for i, dip in enumerate(self._dips):
            if i >= 5:
                break
            else:
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
