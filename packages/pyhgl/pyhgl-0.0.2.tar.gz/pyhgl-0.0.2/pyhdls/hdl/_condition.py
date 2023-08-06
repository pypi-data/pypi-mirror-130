import sys


class When:
    def __init__(self, signal):
        self.caller = sys._getframe(1).f_locals
        if '__hdl_condition__' not in self.caller: 
            self.caller['__hdl_condition__'] = CondFrame()
        self._frame = self.caller['__hdl_condition__']
        self._cond = signal
    def __enter__(self):
        self._frame.new()
        self._frame.tail().when(self._cond)
        self._frame.update()
    def __exit__(self, exc_type, exc_value, traceback):
        self._frame.back()
        self._frame.update()
    
class Otherwise:
    def __init__(self):
        self._frame = sys._getframe(1).f_locals['__hdl_condition__']
    def __enter__(self):
        self._frame.forward()
        self._frame.tail().otherwise()
        self._frame.update()
    def __exit__(self, exc_type, exc_value, traceback):
        self._frame.back()
        self._frame.update()
    
    
class Elsewhen:
    def __init__(self, signal):
        self._frame = sys._getframe(1).f_locals['__hdl_condition__']
        self._cond = signal
    def __enter__(self):
        self._frame.forward()
        self._frame.tail().elsewhen(self._cond)
        self._frame.update()
    def __exit__(self, exc_type, exc_value, traceback):
        self._frame.back()   
        self._frame.update()
    
class CondList:
    def __init__(self):
        self.stack = []   # List[tuple[signal, bool]]
    def when(self, signal):
        self.stack.append((signal, True))
    def elsewhen(self, signal):
        self.otherwise()
        self.when(signal)
    def otherwise(self):
        last, _ = self.stack.pop()
        self.stack.append((last, False))
        
    
class CondFrame:
    def __init__(self):
        self.condlists: List[CondList] = []  # level0, level1, level2
        self.cache: CondList = None 
        
        self.conds = []
        
    def new(self):
        self.condlists.append(CondList())
    def back(self):
        self.cache = self.condlists.pop()
    def forward(self):
        if self.cache is not None:
            self.condlists.append(self.cache)
            self.cache = None 
        else:
            raise Exception("condition does not match")
    def tail(self)->CondList:
        return self.condlists[-1]
    def update(self):
        self.conds = []
        for l in self.condlists:
            self.conds += l.stack
    
    def __str__(self):
        return str(['{}{}'.format('' if x else '!',signal.__hdl_name__()) for signal, x in self.conds])
    

        
        
         
