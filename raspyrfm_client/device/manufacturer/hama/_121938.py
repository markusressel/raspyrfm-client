from raspyrfm_client.device import actions
from raspyrfm_client.device.base import Device


class HAMA(Device):
    _sho = 1
    _lon = 5
    _hi = [(_sho, _sho), (_sho, _lon)]
    _lo = [(_sho, _lon), (_sho, _sho)]
    _sync = (_sho, 40)
    _chmap = [_lo + _lo, _lo + _hi, _hi + _lo]
    
    _repetitoins = 6
    _timebase = 250
    _pausedata = 5600 #not really needed, just for keeping reenginering data
    
    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super().__init__(manufacturer_constants.HAMA, manufacturer_constants._121938)
    
    def get_supported_actions(self) -> [str]:
        return [actions.ON, actions.OFF]
        
    def get_channel_config_args(self):
        return {
            'CODE': '[01]{26}$',
            'CH': '[1-3]$'            
        }
        
    def get_pulse_data(self, action: str):
        tuples = []
        
        cfg = self.get_channel_config()
        for bit in cfg['CODE']:
            tuples += self._hi if bit == '1' else self._lo
        
        tuples += self._hi #group
        
        if action is actions.ON:
            tuples += self._lo
        elif action is actions.OFF:
            tuples += self._hi
        
        tuples +=  self._lo + self._lo #dim/ch?
        
        tuples += self._chmap[int(cfg['CH']) - 1]
        
        tuples += [self._sync]
        
        return tuples, self._repetitoins, self._timebase
