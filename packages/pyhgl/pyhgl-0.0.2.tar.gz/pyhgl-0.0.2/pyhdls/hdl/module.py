
from pyhdls.hdl._hdl import *
from pyhdls.hdl.hardware import * 
from pyhdls.hdl.signal import * 
from pyhdls.hdl._condition import *
from pyhdls.hdl.container import *
from pyhdls.hdl import _global





''' 
some decorators
'''

def bundle(f):
    def wrapper(*args, **kwargs):
        drop_list = f.__code__.co_varnames[:f.__code__.co_argcount]
        local_list = f(*args, **kwargs)
        new_dict = {}
        for k, v in local_list.items():
            if (k[0] != '_') and (k not in drop_list) and isinstance(v, (Signal, Container)):
                new_dict[k] = v 
                
        return Bundle(**new_dict) 
    return wrapper
        





def enum(cls):
    ret = {}
    for k, v in cls.__dict__.items():
        if k[0] != '_':
            ret[k] = v 
    n = len(ret)
    width = utils.width_infer(n-1)
    list_key = list(ret.keys())
    for i in range(n):
        ret[list_key[i]] = UInt(i, w = width)
    return Bundle(**ret)






''' 
inout wire only allowed to connect to tri-gate or inout wire 

input wire cannot appear at the left side

'''


def Input(signal: Signal):
    def toInput(atom_signal: Signal):
        ret = atom_signal._new()
        ret._direction = 'input'  
        return ret 
    return Map(signal, f = toInput)

def Output(signal: Signal):
    def toOutput(atom_signal: Signal):
        ret = atom_signal._new()
        ret._direction = 'output' 
        return ret 
    return Map(signal, f = toOutput)

def InOut(signal: Signal):
    def toInOut(atom_signal: Signal):
        ret = atom_signal._new()
        ret._direction = 'inout' 
        return ret 
    return Map(signal, f = toInOut)

def Flip(signal: Signal):
    '''
    do not return copy since _direction may setted 
    '''
    def setflip(atom_signal: Signal):
        atom_signal._flip = not ret._flip
        return atom_signal 
    return Map(signal, f = setflip)


def IO(io: Bundle) -> Bundle:
    ''' 
    apply flip 
    gen wire nodes
    return bundle
    '''
    def f(x: Signal):
        assert x._direction != 'inner', 'io signals shound have direction!'
        ret = Wire(x._new())
        ret._direction = x._direction
        if x._flip:
            if ret._direction == 'input':
                ret._direction = 'output' 
            if ret._direction == 'output':
                ret._direction = 'input'
        return ret
    return Map(io, f = f)



class _Clocks:
    ''' 
    add a clock: Clock.clock50MHz = 5e7
    '''
    def __init__(self):
        self._frequency: Dict[Signal, float] = {}
    def __setattr__(self, name, value):
        if name[0] == '_':
            object.__setattr__(self, name, value)
        elif hasattr(self, name):
            raise Exception("{name} already exists")
        else:
            frequency = float(value)
            object.__setattr__(self, name, Signal()._setname(name))
            self._frequency[getattr(self, name)] = frequency
    def _step(self):
        for clock in self._frequency.keys():
            clock.value = ~clock.value
    def __str__(self):
        ret = ''
        for signal, freq in self._frequency.items():
            ret += f"{signal._name}: freq = {freq} value = {signal.value}\n"
        return ret
        
_global._clocks = _Clocks()
_global._clocks.clock = 5e7
_global._reset = Signal()._setname('reset')

    


class Module(HDL):

    def __init__(self):
        ...
        
    def __post__(self):
        caller = sys._getframe(1).f_locals
        assert 'io' in caller and isinstance(caller['io'], Bundle), "module without io"
        for k, v in caller.items():
            if k[0] != '_' and isinstance(v, (Container, Signal)):
                v._setname(k)
                self.__dict__[k] = v
        # reverse direction
        for i in Flatten(self.io):
            if i._direction == 'input':
                i._direction = 'output'
            elif i._direction == 'output':
                i._direction = 'input'
        
class Circuit(HDL):
    def __init__(self, module):
        
        self.outputs: List[Signal] = []   # only consider output signal
        self.regs: List[Reg] = []
        self.comb_groups: List[List[Node]] = []
        
        for i in Flatten(module.io):
            if i._direction in ['input', 'inout']:
                self.outputs.append(i)
        
        self.rest_signal: List[Signal] = self.outputs[:]
        while len(self.rest_signal) > 0:
            temp = self.rest_signal
            self.rest_signal = []
            self.comb_groups.append([])
            self.curr_comb = self.comb_groups[-1]
            for node in temp:
                self.dfs(node)
            
    def dfs(self, node: Union[Signal, Node]):
        if isinstance(node, Signal):
            if node.driver is None:
                return 
            self.dfs(node.driver)
        elif abs(node.__hdl_visit__) != id(self):   # new  
            if isinstance(node, Reg):
                self.regs.append(node)
                self.rest_signal += node.inputs
                node.__hdl_visit__ = -id(self)      # regard as leaf node, visited
                return 
            else:  # is comb
                node.__hdl_visit__ = id(self)       # visiting
                for subnode in node.inputs:
                    self.dfs(subnode)
                node.__hdl_visit__ = -id(self)      # visited
                self.curr_comb.append(node)
                return 
        else:                                       
            if node.__hdl_visit__ == id(self):      # visiting
                raise Exception("loop detected in combinational logic")
            else:                                   # visited
                return


    def step(self):
        for i in self.regs:
            i.step()
        _global._clocks._step()
        for i in reversed(self.comb_groups):
            for j in i:
                j.forward()
        for i in self.regs:
            i.forward()


    def show(self):
        for i in self.regs:
            print(i, end='')
        for i in reversed(self.comb_groups):
            for j in i:
                print(j, end='')
        for i in self.regs:
            print(i.__hdl_emit2__())


""" 
TODO emit Module level IR (cannot detect circles)
"""

