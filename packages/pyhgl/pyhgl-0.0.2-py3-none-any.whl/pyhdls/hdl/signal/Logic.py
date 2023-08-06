from typing import Any, Dict, List, Optional, Tuple, Union

from pyhdls.hdl._hdl import * 
from pyhdls.hdl import utils

class Logic(Signal):
    '''
    1-D bits
    -------- 
     
    Attributes
    - value, width: basic
    - shape: slice
    - driver = None: leafNode
    - _name: basic
    
    
    '''
    def __init__(self,value: Union[int, str, bool] = 0, w: int = None ):
        super().__init__()
        
        if isinstance(value, (bool,int)):
            self.value = int(value)
            self.width = utils.width_infer(self.value)
        elif isinstance(value, str):
            self.value, self.width, _ = utils.str2int(value)
        else:
            raise Exception("invalid signal input")
        if w is not None:
            assert w >= self.width, f'overflow: {value} with width {w}'
            self.width = w
    
    def __hdl_name__(self):
        if self.driver is None:
            return f"{self.width}'b{utils.int2str(self.value, self.width)}" 
        else:
            return super().__hdl_name__()  
    
    def __hdl_emit__(self):
        value = f"{self.width}'b{utils.int2str(self.value, self.width)}" 
        if self.driver is None:
            return value
        else:
            return f"{self._direction} {self.__hdl_name__()} = {value}"

    def W(length: int):
        assert self.width > length 
        return Slice(self, length-1, 0) 
    
    # TODO
    def View(*shape): ...

    def __invert__(self): 
        return NOT(self)
    
    
    

    
class AND(Node):
    def __init__(self, a: Signal, b: Signal):
        super().__init__()
        if type(b) is str: b = Logic(b)
        self.inputs = [a, b]
        longer = a if a.width > b.width else b
        self.outputs = [longer._new(value=0)]
        self.outputs[0].driver = self

    def forward(self):
        self.outputs[0].value = self.inputs[0].value & self.inputs[1].value


class OR(Node):

    def __init__(self, a: Signal, b: Signal):
        super().__init__()
        if type(b) is str: b = Logic(b)
        self.inputs = [a, b]
        longer = a if a.width > b.width else b
        self.outputs = [longer._new(value=0)]
        self.outputs[0].driver = self

    def forward(self):
        self.outputs[0].value = self.inputs[0].value | self.inputs[1].value


class NOT(Node):

    def __init__(self, a: Signal):
        super().__init__()
        self.inputs = [a]
        self.outputs = [a._new(value=0)]
        self.outputs[0].driver = self

    def forward(self):
        self.outputs[0].value = ~self.inputs[0].value


class XOR(Node):

    def __init__(self, a: Signal, b: Signal):
        super().__init__()
        if type(b) is str: b = Logic(b)
        self.inputs = [a, b]
        longer = a if a.width > b.width else b
        self.outputs = [longer._new(value=0)]
        self.outputs[0].driver = self

    def forward(self):
        self.outputs[0].value = self.inputs[0].value ^ self.inputs[1].value




class Mux(Node):
    '''
    2 to 1 mux 
    sel != 0: first
    else: second
    '''

    def __init__(self, sel: Signal, first: Signal, second: Signal):
        super().__init__()
        if type(first) is str: first = Logic(first)
        if type(second) is str: second = Logic(second)
        self.inputs = [sel, first, second]
        longer = first if first.width > second.width else second
        self.outputs = [longer._new(value=0)]
        self.outputs[0].driver = self

    def forward(self):
        self.outputs[0].value = self.inputs[1].value if self.inputs[0].value != 0 else self.inputs[2].value


class Cat(Node):
    def __init__(self, *args: Signal):
        super().__init__()
        assert len(args) > 0, 'no input'
        self.inputs = []
        width = 0 
        for i in args:
            if type(i) is str: i = Logic(i)
            self.inputs.append(i)
            width += i.width
        self.outputs = [args[0]._new(value=0, width=width)]
        self.outputs[0].driver = self

    def forward(self):
        value = 0
        for i in self.inputs:
            value = (i.value & ((1 << i.width) - 1)) | (value << i.width)
        self.outputs[0].value = value


class Slice(Node):
    ''' 
    apply slice on 1-D bits 
    1111_0000
    ^^^^ ^^^^
    7654 3210
    
    return bits from start to end, including endpoint
    if start < end, reversed order
    '''
    def __init__(self, driver: Signal, start: int, end: int = None):
        super().__init__()
        if not end:
            end = start
        assert start >= 0 and start < driver.width 
        assert end >= 0 and end < driver.width 
        
        width = abs(start - end) + 1
        self.inputs = [driver]
        self.outputs = [driver._new(value=0, width=width)]     
        self.outputs[0].driver = self
        self._start = start
        self._end = end

    def __hdl_emit__(self):
        left = self.outputs[0].__hdl_name__()
        right = self.inputs[0].__hdl_name__()
        return f"{left} = {right}[{self._start}:{self._end}]"


    def forward(self):
        value = self.inputs[0].value
        width = self.outputs[0].width
        n_shift = min(self._end, self._start)
        value = (value >> self._end) & ((1 << width) - 1)
        if self._start >= self._end:
            self.outputs[0].value = value 
        else:
            # reverse 
            real_value = 0 
            for i in range(width):
                real_value <<= 1
                real_value += value & 1 
                value >>= 1
            self.outputs[0].value = real_value 




