from raspyrfm_client.device_implementations.controlunit.actions import Action
from raspyrfm_client.device_implementations.controlunit.base import ControlUnit


class HX2262Compatible(ControlUnit):
    _sho = 1
    _lon = 3

    _d0 = [(_sho, _lon), (_sho, _lon)]
    _d1 = [(_lon, _sho), (_lon, _sho)]
    _df = [(_sho, _lon), (_lon, _sho)]

    _sync = (_sho, 31)

    _repetitions = 5
    _timebase = 350
    _pausedata = 5600  # not really needed, just for keeping reenginering data

    from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer
    from raspyrfm_client.device_implementations.controlunit.controlunit_constants import ControlUnitModel

    def __init__(self, manufacturer: Manufacturer = Manufacturer.UNIVERSAL,
                 model: ControlUnitModel = ControlUnitModel.HX2262):
        super().__init__(manufacturer, model)

    def get_supported_actions(self) -> [Action]:
        return [Action.ON]

    def get_channel_config_args(self):
        return {
            '1': '^[01fF]$',
            '2': '^[01fF]$',
            '3': '^[01fF]$',
            '4': '^[01fF]$',
            '5': '^[01fF]$',
            '6': '^[01fF]$',
            '7': '^[01fF]$',
            '8': '^[01fF]$',
            '9': '^[01fF]$',
            '10': '^[01fF]$',
            '11': '^[01fF]$',
            '12': '^[01fF]$'
        }

    def get_pulse_data(self, action: Action):
        bitdata = self.get_bit_data(action)

        # print("bits:", bitdata[0])

        if len(bitdata[0]) != 12:
            raise ValueError("Bits not configured")

        tuples = []

        for bit in bitdata[0]:
            bit_value = bit.lower()
            if bit_value == 'f':
                tuples += self._df
            elif bit_value == '0':
                tuples += self._d0
            elif bit_value == '1':
                tuples += self._d1
            else:
                raise ValueError(
                    "Invalid bit value \"" + bit_value + "\"! Must be one of ['0', '1', 'f'] (case insensitive)")

        tuples.append(self._sync)  # sync pulse

        return tuples, bitdata[1], self._timebase

    def get_bit_data(self, action: Action):
        """
        This method should be implemented by inheriting classes
        :return: char array (12 bits '0'|'1'|'f'), number of repetitions
        """

        cfg = self.get_channel_config()
        bits = []

        for i in range(12):
            bits += cfg[str(i + 1)]

        return bits, self._repetitions

    def calc_int_bits(self, value, num_bits, bitvalues):
        """
        converts an integervalue to a bitarray using binary format
        :param value: integer to convert
        :param num_bits: number of bits to convert
        :param bitvalues: tuples of low- and highvalue to use for the array
        
        :return:
        array if given bitvalues
        """
        bits = []
        for i in range(num_bits):
            bits.append(bitvalues[1] if (value & 1 << i) != 0 else bitvalues[0])
        return bits

    def calc_match_bits(self, value, num_bits, bitvalues):
        """
        converts an integervalue to a bitarray, only bit nr. value will be set
        :param value: integer to convert
        :param num_bits: number of bits to convert
        :param bitvalues: tuples of low- and highvalue to use for the array
        
        :return:
        array if given bitvalues
        """
        bits = []
        for i in range(num_bits):
            bits.append(bitvalues[1] if value == i else bitvalues[0])
        return bits
