from .Logic import *


class SInt(Logic):
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
            self.width = utils.width_infer(self.value, signed=True)
        elif isinstance(value, str):
            self.value, self.width, _ = utils.str2int(value, signed=True)
        else:
            raise Exception("invalid signal input")

        if w is not None:
            assert w >= self.width, f'overflow: {value} with width {w}'
            self.width = w
    
        
    # TODO
    # def __getitem__(self, key):
    #     if isinstance(key, str):
    #         return copy.copy(self.value[key])
    #     if isinstance(key, int):
    #         return copy.copy(self.value[self._keys[key]])
    #     if isinstance(key, slice):
    #         # return a bundle 
    #         new_dict = {}
    #         for k in self._keys[key]:
    #             new_dict[k] = self.value[k]
    #         return Bundle(**new_dict)
    #     raise Exception(f"key error: {key}")

    
    # def __deepcopy__(self,memo):
    #     cls = self.__class__
    #     ret = cls.__new__(cls)
    #     ret.__dict__.update(self.__dict__)
    #     ret.driver = None 
    #     ret._name = ""
    #     return ret
 