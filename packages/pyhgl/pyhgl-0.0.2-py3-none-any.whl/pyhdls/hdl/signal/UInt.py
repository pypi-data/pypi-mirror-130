from .Logic import *



class UInt(Logic):
    ''' 
    '''
    def __init__(self,value: Union[int, str, bool] = 0, w: int = None):
        super().__init__()
        # basic attribute
        self.value: int = 0 
        self.width: int = 1 
        self.shape: Tuple[int, ...] = None
        # leaf node ? 
        self.driver = None   
        self._name = ""
        # for input output 
        self._flip = False 
        self._direction = 'inner'
        
        if isinstance(value, (bool,int)):
            self.value = int(value)
            self.width = utils.width_infer(self.value)
        elif isinstance(value, str):
            assert value[0] not in ['$', '+', '-'], 'UInt not accept signed value'
            self.value, self.width, _ = utils.str2int(value)
        else:
            raise Exception("invalid signal input")

        if w is not None:
            assert w >= self.width, f'overflow: UInt({value}) with width {w}'
            self.width = w
    
    