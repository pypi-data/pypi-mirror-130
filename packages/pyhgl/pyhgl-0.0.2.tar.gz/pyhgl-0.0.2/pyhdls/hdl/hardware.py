
from typing import Any, Dict, List, Optional, Tuple, Union

from pyhdls.hdl._hdl import *
from pyhdls.hdl import _global
from pyhdls.hdl.signal import Logic


"""   
basic hardware nodes
    Wire: signal pass 
    Reg: signal store 
    WireInOut
    Mux: 2 to 1 mux
"""


class Wire(Node):

    def __init__(self, driver: Signal):
        super().__init__()
        assert isinstance(driver, Signal)
        self.inputs = [driver]
        self.outputs = [driver._new(value=0)]    # no value, only width
        self.outputs[0].driver = self

    def __new__(cls, driver):
        if isinstance(driver, Container):
            return Map(driver, f = Wire)
        else:
            ret = object.__new__(cls)
            ret.__init__(driver)
            return ret.outputs[0]    # return Signal

    def forward(self):
        self.outputs[0].value = self.inputs[0].value


class Reg(Node):

    def __init__(self, driver: Signal, init: Signal = None, reset=None, clock=None, posedge=True):
        ''' 
        reset & clock: Signal
        '''
        super().__init__()
        assert isinstance(driver, Signal)
        if reset is None:
            reset: Signal = _global._reset
        if clock is None:
            clock: Signal = _global._clocks.clock
        if init is None:
            init = driver._new(value=0)

        self.inputs = [driver, init, reset, clock]
        self.outputs = [driver._new(value=0)]
        self.outputs[0].driver = self
        self.outputs[0].value = init.value
        # for step
        self.curr_value = None
        self.curr_clock = None
        self.prev_clock = None
        self.posedge = posedge

    def __new__(cls, driver, *args, **kwargs):
        if isinstance(driver, Container):
            return Map(driver, f = Reg)
        else:
            reg = object.__new__(cls)
            reg.__init__(driver, *args, **kwargs)
            return reg.outputs[0]    # return Signal

    def __hdl_emit__(self):
        left = self.outputs[0].__hdl_name__()
        driver, init, reset, clock = self.inputs
        return f"{left} = Reg({init.__hdl_name__()}, {reset.__hdl_name__()}, {clock.__hdl_name__()})"
    
    def __hdl_emit2__(self):
        return self.outputs[0].__hdl_name__() + ' <= ' + self.inputs[0].__hdl_name__()

    def forward(self): 
        self.curr_value = self.inputs[0].value
        self.prev_clock = self.curr_clock 
        self.curr_clock = self.inputs[3].value != 0
         
    def step(self): 
        if self.inputs[2].value != 0:  # reset
            self.outputs[0].value = self.outputs[1].value
            return
        if self.prev_clock is not None and self.curr_clock is not None:
            if self.posedge:
                if not self.prev_clock and self.curr_clock:
                    self.outputs[0].value = self.curr_value
            else:
                if self.prev_clock and not self.curr_clock:
                    self.outputs[0].value = self.curr_value
         

class WireInOut(Node):
    ''' 
    inputs: [sel, signal, sel, signal, ...]
    outputs: [signal, signal, ...]
    '''
    def __init__(self, x: Signal):
        super().__init__()
        assert x._direction == 'inout', 'inout wire needs inout signal'
        self.inputs = []
        self.outputs = [x._new(value=0)]
        self.outputs[0].driver = self
        self.default_value = x.value
        
    def __new__(cls, x):
        if isinstance(x, Container):
            return Map(x, f = WireInOut)
        else:
            ret = object.__new__(cls)
            ret.__init__(x)
            return ret.outputs[0]     
        
    def _merge(self, other):
        assert isinstance(other, WireInOut) and self.outputs[0].width == other.outputs[0].width 
        self.inputs += other.inputs
        self.outputs += other.outputs 
        for signal in self.inputs + self.outputs:
            signal.driver = self
        
    def forward(self):
        value = None 
        for i in range(len(self.inputs)/2):
            if self.inputs[i*2].value != 0:   # select that value
                if value is None:
                    value = self.inputs[i*2+1].value
                else:
                    raise Exception("simulation error: multiple driver of inout wire")
        if value is None:
            value = x.vlaue
        for i in self.outputs:
            i.value = value
        
        
        
def Tri(sel: Signal, driver: Signal, inout: Signal) -> Union[Signal, Container]:
    ''' 
    sel:   if sel, inout <= driver; else inout <= high-z

    return: output signal of the inout wire
    '''            
    if isinstance(inout, Container):
        return Map(sel, driver, inout, f=Tri)
    else:
        assert isinstance(inout, Signal) and inout._direction == 'inout' and isinstance(inout.driver, WireInOut)
        assert isinstance(sel, Signal)
        assert isinstance(driver, Signal)
        inout.driver.inputs.extend([sel, dirver])
        return inout.driver.outputs[0]
        
    



class _Mux(Node):
    '''
    2 to 1 mux used in conditional assignment
    do not use it explictly!
    if sel, return first
    '''

    def __init__(self, sel: Signal, first: Signal, second: Signal):
        super().__init__()
        self.inputs = [sel, first, second]
        longer = first if first.width > second.width else second
        self.outputs = [longer._new(value=0)]
        self.outputs[0].driver = self

    def forward(self):
        self.outputs[0].value = self.inputs[1].value if self.inputs[0].value != 0 else self.inputs[2].value


# conditional assignment

def _condwalker(inports: List[Signal], idx: int, conds:list, new_signal: Signal):
    ''' 
    inports[idx]: Wire.inputs[0] | Reg.inputs[0] | _Mux.inputs[1] | _Mux.inputs[2]
    
    conds: [(c0, True), (c1, False), ...]
    '''
    if len(conds) == 0:
        inports[idx] = new_signal 
        return 
    
    default_signal = inports[idx]
    cond_signal, cond_sel = conds[0]
    
    if isinstance(default_signal.driver, _Mux) and default_signal.driver.inputs[0] is cond_signal:
        pass # do not generate new mux 
    else:
        inports[idx] = _Mux(cond_signal, default_signal, default_signal)  # new mux takes default signal
    # goto _Mux
    _condwalker(inports[idx].driver.inputs, int(not cond_sel)+1, conds[1:], new_signal)



def _update(left: Union[Signal, Container], right: Union[Signal, Container, str], conds:list) -> None:
    ''' 
    left: Signal  or their Container  
    right: Signal or their Container  
    
    !!! notice: assignment operator should always return left side 
    '''
    if isinstance(left, Container):
        Map(left, right, conds, f = _update_element)
    # is logic
    _update_element(left, right, conds)
        
def _update_element(left: Signal, right: Union[Signal, str], conds: list) -> None:
    if type(right) is str: 
        right = Logic(right)
    assert isinstance(left, Signal) and isinstance(right, Signal), "update nonsignal"
    # conditional update
    if left._direction not in ['input', 'inout'] and right._direction != 'inout':
        _condwalker(left.driver.inputs, 0, conds, right) 
    # inout connection
    elif left._direction == 'inout' and right._direction == 'inout':
        left.driver._merge(right.driver) 
    else:
        raise Exception(f"Error: {left._direction} <<= {right._direction}")
    
__hdl_op__['__ilshift__'].default = _update


