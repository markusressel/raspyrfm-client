from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device


class HX2262Compatible(Device):
    _lo = 1
    _hi = 3
    _seqLo = [(_lo, _hi), (_lo, _hi)]
    _seqHi = [(_hi, _lo), (_hi, _lo)]
    _seqFl = [(_lo, _hi), (_hi, _lo)]

    _bits = []
    
    _connair_params = {'repetitions': 5, 'pauselen': 5600, 'steplen': 375}

    from raspyrfm_client.device.manufacturer import manufacturer_constants
    def __init__(self, manufacturer: str = manufacturer_constants.UNIVERSAL, model: str = manufacturer_constants.HX2262):
        super().__init__(manufacturer, model)

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def set_bits(self, bits: []):
        self._bits = bits

    def generate_code(self, action: str = None) -> str:
        tuples = []
        
        if len(self._bits) != 12:
            raise ValueError("Bits not configured")
        
        for bit in self._bits:
            bit_value = bit.lower()
            if bit_value == 'f':
                tuples += self._seqFl
            elif bit_value == '0':
                tuples += self._seqLo
            elif bit_value == '1':
                tuples += self._seqHi
            else:
                raise ValueError(
                    "Invalid dip value \"" + bit_value + "\"! Must be one of ['0', '1', 'f'] (case insensitive)")
        
        tuples.append( (1, 31) )  #sync pulse
        
        return super().generate_conair_code(tuples)
