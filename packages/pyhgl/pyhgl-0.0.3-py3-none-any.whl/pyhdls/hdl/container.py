from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import copy

from pyhdls.hdl._hdl import *




class Vec(Container):
    """
    n-D array of any signal, hardware, Vec, Bundle, or other python types
    
    init: 
        array like, len >= 1
        save copys 
    
    """
    
    def __init__(self, array):
        
        super().__init__()
        
        if isinstance(array, list):
            array = np.array(array, dtype=object)

        assert isinstance(array, np.ndarray), "Vec input should be array like"
        assert len(array) > 0, "empty Vec"
                
        self._shape: Tuple[int] = array.shape
        elements = []
        for i in array.flat: 
            elements.append(copy.copy(i))
        self._value = np.array(elements, dtype=object).reshape(self._shape)
        
        
    def _new(self, array: list):
        assert len(array) == len(self), 'length mismatch'
        return Vec(np.array(array, dtype=object).reshape(self._shape))
        
    def _flat(self):
        return self._value.flat
        
    @staticmethod
    def Full(shape, value):
        return Vec(np.full(shape, value, dtype = object))


    def _setname(self, name):
        for i, v in enumerate(self._value.flat):
            if isinstance(v, (Signal, Container)):
                v._setname(name + '_' + str(i))

    def __hdl_emit__(self):
        ret = f"{self.__hdl_name__()}{self._shape}" + "{\n"
        for i in self._value.flat:
            if isinstance(i, HDL):
                ret += i.__str__(1)
            else:
                ret += f"  {i}\n"
        return  ret + '}'
    
    def __len__(self):
        return len(self._value.flat)
       
    def __getitem__(self, key):
        single = True 
        if type(key) is tuple:
            for i in key:
                if type(i) is not int:
                    single = False 
        elif type(key) is not int:
            single = False
        return copy.copy(self._value[key]) if single else Vec(self._value[key])
    
    def __setitem__(self, key, value):
        self._value.__setitem__(key, value)
    
    def __copy__(self):
        return Vec(self._value)


class Bundle(Container):
    '''
    container of any signal, hardware, Vec, Bundle, or other python types
    init:
        named arguments 
        store copy
    getitem: 
        support int, slice, string
        return copy
    setitem:
        only string or int for existed key
    setattr:
        only for existed key
        
    '''
    
    def __init__(self, **args):
        
        super().__init__()
        self._value = {}
        self._keys: List[str] = []
        
        for k, v in args.items():
            # name start with _ will be ignored
            if k[0] == '_':
                continue       
            self._value[k] = copy.copy(v)
            self._keys.append(k)
        self.__dict__.update(self._value)

    def _new(self, array: list):
        assert len(array) == len(self), 'length mismatch'
        new_dict = dict(zip(self._keys, array))
        return Bundle(**new_dict)
        
    def _flat(self):
        return self._value.values()
        

    def _setname(self, name):
        for k, v in self._value.items():
            if isinstance(v, (Signal, Container)):
                v._setname(name + '_' + k)
    # return readable string
    def __hdl_emit__(self):
        ret = self.__hdl_name__() + "{\n"
        for k, v in self._value.items():
            if isinstance(v, HDL):
                ret = ret + v.__str__(1, prefix = f"{k}: ")  
            else:
                ret += "  " + f"{k}: {v}\n"
        return ret + "}"
    
    def __len__(self):
        return len(self._keys)
    
    def __getitem__(self, key):
        if isinstance(key, str):
            return copy.copy(self._value[key])
        if isinstance(key, int):
            return copy.copy(self._value[self._keys[key]])
        if isinstance(key, slice):
            # return a bundle 
            new_dict = {k:self._value[k] for k in self._keys[key]}
            return Bundle(**new_dict)
        
        raise Exception(f"key error: {key}")
    
    def __setitem__(self, key, value):
        if isinstance(key, int):
            key = self._keys[key]
        assert key in self._keys, f"unknown key {key}"
        # update both dict
        self._value[key] = value
        self.__dict__[key] = value
    
    def __setattr__(self, key, value):
        # unexisted key is not allowed
        if key[0] == '_':
            object.__setattr__(self, key, value)
        elif key in self._keys:
            self._value[key] = value
            self.__dict__[key] = value
        else:
            raise Exception(f"unknown key {key}")
    
    def __copy__(self):
        return Bundle(**self._value)
        

    
def Flatten(x: Container) -> list:
    if not isinstance(x, Container):
        return [x]
    ret = []
    for i in x._flat():
        ret += Flatten(i)
    return ret

def Zip(*args):
    return Map(*args, f = lambda *x: x)


# TODO 
def Filter(f, x: Container): ...
    


