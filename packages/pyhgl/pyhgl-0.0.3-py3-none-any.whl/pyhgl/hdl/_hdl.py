
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import sys

__all__ = ['HDL', 'Container', 'Map', '__hdl_op__', 'Signal', 'Node']

class HDL:
    ''' 
    internal methods
    ----------------
    '''
    def __init__(self): 
        self._name: str = ''
        
    def __hdl_version__(self): 
        return (0,0,1)
    
    def _setname(self, name: str = ''):         raise Exception("not implemented") 
    def __hdl_name__(self):                     raise Exception("not implemented") 
    
    # return string with intend and prefix 
    def __str__(self, intend = 0, prefix = ''):
        s = self.__hdl_emit__().splitlines(keepends=True)
        return "  "*intend + prefix + ("  "*intend).join(s) + '\n'
    def __hdl_emit__(self):                     raise Exception("not implemented")
    
    # because __bool__ can only return True/False, to return HDL, use: when (a == 0 | b != 0): ...
    def __bool__(self):                         raise Exception("bool is not allowed")     
    def __copy__(self): return self      
    def __hash__(self): return id(self)
    
    '''
    special operators & unary operators
    -----------------------------------
    '''
    def __getitem__(self, args):                raise Exception("not implemented")
    def __setitem__(self, key, value):          raise Exception("not implemented")
     # a**2   duplicate bits
    def __pow__(self, other):                   raise Exception("not implemented")       
    def __bytes__(self):                        raise Exception("not implemented")   
    
    def __len__(self):                          raise Exception("not implemented")           
    def __invert__(self):                       raise Exception("not implemented")           
    def __abs__(self):                          raise Exception("not implemented")           
    def __pos__(self):                          raise Exception("not implemented")           
    def __neg__(self):                          raise Exception("not implemented")               
    

    ''' 
    external binary operators
    -------------------------
    overload of python binary operators like: +-*/|&
    only for Logic/Contianer Type
    '''
    # bitwise
    def __or__(self, other):        return __hdl_op__['__or__'].apply(self, other)      # a | b
    def __and__(self, other):       return __hdl_op__['__and__'].apply(self, other)     # a & b
    def __xor__(self, other):       return __hdl_op__['__xor__'].apply(self, other)     # a ^ b
    def __lshift__(self, other):    return __hdl_op__['__lshift__'].apply(self, other)  # a << b
    def __rshift__(self, other):    return __hdl_op__['__rshift__'].apply(self, other)  # a >> b
    
    # used for comparison, return 1-bit signal
    def __lt__(self, other):        return __hdl_op__['__lt__'].apply(self, other)      # a < b
    def __gt__(self, other):        return __hdl_op__['__gt__'].apply(self, other)      # a > b
    def __le__(self, other):        return __hdl_op__['__le__'].apply(self, other)      # a <= b
    def __ge__(self, other):        return __hdl_op__['__ge__'].apply(self, other)      # a >= b
    def __eq__(self, other):        return __hdl_op__['__eq__'].apply(self, other)      # a == b
    def __ne__(self, other):        return __hdl_op__['__ne__'].apply(self, other)      # a != b
    # calculate
    def __add__(self, other):       return __hdl_op__['__add__'].apply(self, other)     # a + b
    def __sub__(self, other):       return __hdl_op__['__sub__'].apply(self, other)     # a - b
    def __mul__(self, other):       return __hdl_op__['__mul__'].apply(self, other)     # a * b
    def __matmul__(self, other):    return __hdl_op__['__matmul__'].apply(self, other)  # a @ b
    def __truediv__(self, other):   return __hdl_op__['__truediv__'].apply(self, other) # a / b
    def __mod__(self, other):       return __hdl_op__['__mod__'].apply(self, other)     # a % b
    def __floordiv__(self, other):  return __hdl_op__['__floordiv__'].apply(self,other) # a // b
    
    '''
    assignment & connection
    -----------------------
    always return self !!!
    '''
    
    # hdl assignment <<=, like assign a = b in systemverilog
    def __ilshift__(self, other):  
        caller = sys._getframe(1).f_locals
        if '__hdl_condition__' not in caller:
            conds = []  
        else:
            conds = caller['__hdl_condition__'].conds
        __hdl_op__['__ilshift__'].apply(self, other, conds)         
        return self  
    
    def __iadd__(self, other):      __hdl_op__['__iadd__'].apply(self, other);      return self # +=
    def __isub__(self, other):      __hdl_op__['__isub__'].apply(self, other);      return self # -=
    def __imul__(self, other):      __hdl_op__['__imul__'].apply(self, other);      return self # *=  
    def __imatmul__(self, other):   __hdl_op__['__imatmul__'].apply(self, other);   return self # @=           
    def __ifloordiv__(self, other): __hdl_op__['__ifloordiv__'].apply(self, other); return self # //=
    def __itruediv__(self, other):  __hdl_op__['__itruediv__'].apply(self, other);  return self # /=
    def __imod__(self, other):      __hdl_op__['__imod__'].apply(self, other);      return self # %= 
    def __ipow__(self,other):       __hdl_op__['__ipow__'].apply(self, other);      return self # **=
    def __irshift__(self, other):   __hdl_op__['__irshift__'].apply(self, other);   return self # >>=
    def __iand__(self, other):      __hdl_op__['__iand__'].apply(self, other);      return self # &=
    def __ior__(self, other):       __hdl_op__['__ior__'].apply(self, other);       return self # |=
    def __ixor__(self, other):      __hdl_op__['__ixor__'].apply(self, other);      return self # ^=



class Container(HDL):
    ''' 
    features:
      - len(a) return number of elements 
      - support index a[idx]
    '''
    def __init__(self):
        super().__init__()
        
    def __hdl_name__(self): return self.__class__.__name__  
    
    def _flat(self): ...  # return an itelator
    
    def _new(self, array: list): ... # input a list, return new instance with same shape
        
def Map(*args, f = None):
    ''' 
    map functions on containers 
    '''
    first = None
    for arg in args:
        if isinstance(arg, Container):
            if first is None:
                first = arg 
            else:
                assert len(first) == len(arg), "shape mismatch!"
    if first is None:   # no containers
        return f(*args)
    # extract containers
    new_elements = []
    for n in range(len(first)):
        arg_list = []
        for arg in args:
            if isinstance(arg, Container):
                arg_list.append(arg[n])
            else:
                arg_list.append(arg)
        new_elements.append(f(*arg_list))
    return first._new(new_elements)
        


    
'''
operator behavior:
unary_op:
    if not implemented, call base class 
binary_op:
    1. search registered functions for that operator
    2. apply default function if defined
    3. otherwise deal with container
    4. raise error
'''
class __hdl_op__:
    class Operator:
        def __init__(self, name:str):
            self.name = name 
            self.default = None
            self.table = {}    # a table of functions

        def find(self, l, r):
            if l not in self.table: self.table[l] = {}
            if r not in self.table[l]: self.table[l][r] = None     
            return self.table[l][r]    
           
        def _register(self, f, left: type, right: type):
            l = left.__name__
            r = right.__name__
            self.find(l, r)
            self.table[l][r] = f 
            
        def register(self, left: type, f, *right: type, order = 'normal' ):
            assert order in ['normal', 'inverse', 'both']
            if order in ['normal','both']:
                for r in right:
                    self._register(f, left, r)
            if order in ['inverse', 'both']:
                for r in right:
                    self._register(f, r, left)
            
        def apply(self, left, right, *args) -> Any:
            l = left.__class__.__name__
            r = right.__class__.__name__
            f = self.find(l, r)
            if f is not None: 
                return f(left, right, *args)
            if self.default is not None:
                return self.default(left, right, *args)
            if isinstance(left, Container) or isinstance(right, Container): 
                return Map(left, right, *args, f = lambda x,y: getattr(x, self.name)(y))
            raise Exception(f"{l}{self.name}{r} not defined")
        
        def __str__(self):
            return self.name + ' ' + str(self.table) + '\n'
            
    def __init__(self):
        self.op: Dict[str, __hdl_op__.Operator] = {}     
    def __getitem__(self, key:str):
        assert len(key) > 4 and key[:2] == '__' and key[-2:] == '__'
        if key not in self.op:
            self.op[key] = __hdl_op__.Operator(key)
        return self.op[key]
    def __str__(self):
        ret = ''
        for i in self.op.values():
            ret += str(i)
        return ret

__hdl_op__ = __hdl_op__()

__names__: Set[str] = set()

class Signal(HDL):
    def __init__(self, value: int = 0, width:int = 1):
        super().__init__()
        # basic attribute
        self.value: int = value 
        self.width: int = width
        self.driver: Node = None   
        # for io and assignment
        self._flip: bool = False 
        self._direction = 'inner'      
          
    def _set(self, value: int = 0):
        self.value = value       
         
    def _new(self, value: int = None, width: int = None):
        ''' 
        parameter: 
          1. value
          2. width
        return a new instance without other attributes
        like copy
        '''
        if value is None: value = self.value
        if width is None: width = self.width 
        return self.__class__(value, width)

    def _setname(self, name: str = ''):
        # do not set
        if len(self._name) > 0: 
            return self 
        # set name
        if len(name) > 0 and name not in __names__:
            self._name = name         
        else:
            if len(name) == 0:
                name = self.__class__.__name__            
            n = 1 
            while name + '_' + str(n) in __names__: n += 1
            name = name + '_' + str(n) 
            self._name = name
        __names__.add(self._name)
        return self

    def __hdl_name__(self):
        if len(self._name) == 0: 
            self._setname()
        return self._name  

    def __hdl_emit__(self):
        return str(self.value)

class Node(HDL):
    ''' 
    hardware that outputs relays on inputs
    no operators on Node is allowed!
    return signal only
    '''
    def __init__(self):
        super().__init__()
        self.__hdl_visit__:int = 0       # travel DAG 
        self.inputs: List[Signal] = []   # wires
        self.outputs: List[Signal] = []  # wires
    
    def __hdl_name__(self): return self.__class__.__name__  
    def __hdl_emit__(self):
        left = ','.join([i.__hdl_name__() for i in self.outputs])
        right = ','.join([i.__hdl_name__() for i in self.inputs])
        return left + ' = ' + self.__hdl_name__() + '(' + right + ')' 

    def __new__(cls, *args, **kwargs):
        # return a signal, not node
        node = object.__new__(cls)
        node.__init__(*args, **kwargs)
        return node.outputs[0]


    def forward(self):  raise Exception("not implemented")  
    def step(self):     raise Exception("not implemented")  
        
