from raspyrfm_client.device import actions
from raspyrfm_client.device.manufacturer.elro.AB440S import AB440S


class AB440ID(AB440S):
    _dips = ['1', '2', '3', '4', '5', '6', '7', '8']

    def __init__(self):
        from raspyrfm_client.device.manufacturer import manufacturer_constants
        super(AB440S, self).__init__(manufacturer_constants.ELRO, manufacturer_constants.AB440ID)

    def generate_code(self, action: str) -> str:
        cfg = self.get_channel_config()
        if cfg is None:
            raise ValueError("Missing channel configuration :(")
        if action not in self.get_supported_actions():
            raise ValueError("Unsupported action: " + action)
            
        bits = []
        
        for i, dip in enumerate(self._dips):
            if i < 5:
                continue
            else:
                bits.append('0' if cfg[dip] else 'f')
                
        bits += ['f', 'f']
        
        for i, dip in enumerate(self._dips):
            if i >= 5:
                break
            else:
                bits.append('0' if cfg[dip] else 'f')
        
        if action is actions.ON:
            bits += self._on
        elif action is actions.OFF:
            bits += self._off
        else:
            raise ValueError("Invalid action")
            
        super().set_bits(bits)
        print(bits)
            
        return super(AB440S, self).generate_code()