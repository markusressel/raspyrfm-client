from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device


class Ec000x(Device):
    _on = ['0', '1']
    _off = ['1', '0']
    
    _lo = 1
    _hi = 3
    _seqLo = [(_lo, _hi)]
    _seqHi = [(_hi, _lo)]
    _sync = [(1, 31)]
    
    _connair_params = {'repetitions': 5, 'pauselen': 5600, 'steplen': 300}
    
    _chvalues = [
        _seqHi + _seqHi + _seqHi,
        _seqLo + _seqHi + _seqHi,
        _seqHi + _seqLo + _seqHi,
        _seqHi + _seqHi + _seqLo
    ]
    
    _argchecks = {
        'CODE': '[0-9A-F]{5}$',
        'CH': '[1-4]$'
    }

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.LOGILINK, manufacturer_constants.EC000X)

    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF, actions.PAIR]
        
    def get_pulse_data(self, action: str):
        cfg = self.get_channel_config()
        tuples = []
        for nibble in cfg['CODE']:
            val = int(nibble, 16)
            for i in range(4):
                if (val & 0x8) > 0:
                    tuples += self._seqHi
                else:
                    tuples += self._seqLo
                val <<= 1
                
        if action is actions.ON:
            tuples += self._seqHi
            self._connair_params['repetitions'] = 5
        elif action is actions.PAIR:
            tuples += self._seqHi
            self._connair_params['repetitions'] = 15
        elif action is actions.OFF:
            tuples += self._seqLo
            self._connair_params['repetitions'] = 5
            
        tuples += self._chvalues[int(cfg['CH']) - 1]
                  
        tuples += self._sync
        print(tuples)
        return tuples
        