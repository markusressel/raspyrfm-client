from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device


class HX2262Compatible(Device):
    _lo = 1
    _hi = 3
    _seqLo = [(_lo, _hi), (_lo, _hi)]
    _seqHi = [(_hi, _lo), (_hi, _lo)]
    _seqFl = [(_lo, _hi), (_hi, _lo)]

    _connair_params = {'repetitions': 5, 'pauselen': 5600, 'steplen': 350}

    from raspyrfm_client.device.manufacturer import manufacturer_constants
    def __init__(self, manufacturer: str = manufacturer_constants.UNIVERSAL, model: str = manufacturer_constants.HX2262):
        super().__init__(manufacturer, model)

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def get_bits(self, action: str):
        """
        This method should be implemented by inheriting classes
        :return: bit array, 12 bits á '0'|'1'|'f'
        """
        raise NotImplementedError
        
    def calc_int_bits(self, value, num_bits):
        bits = []
        for i in range(num_bits):
            bits.append(self._h if (value & 1<<i) != 0 else self._l)
        return bits
        
    def calc_match_bits(self, value, num_bits):
        bits = []
        for i in range(num_bits):
            bits.append(self._h if value == i else self._l)
        return bits
        
    def calc_dip_bits(self, dips):
        cfg = self.get_channel_config()
        bits = []
        for dip in dips:
            bits.append(self._h if cfg[dip] else self._l)
        return bits
        
    def get_pulse_data(self, action: str):
        bits = self.get_bits(action)
        
        if len(bits) != 12:
            raise ValueError("Bits not configured")
            
        tuples = []
        
        for bit in bits:
            bit_value = bit.lower()
            if bit_value == 'f':
                tuples += self._seqFl
            elif bit_value == '0':
                tuples += self._seqLo
            elif bit_value == '1':
                tuples += self._seqHi
            else:
                raise ValueError(
                    "Invalid bit value \"" + bit_value + "\"! Must be one of ['0', '1', 'f'] (case insensitive)")
        
        tuples.append( (1, 31) )  #sync pulse
        
        return tuples

class HX2262DipDevice(HX2262Compatible):
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
        
    def get_bits(self, action: str):
        bits = []
        
        bits += self.calc_dip_bits(self._dips)
        
        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        return bits