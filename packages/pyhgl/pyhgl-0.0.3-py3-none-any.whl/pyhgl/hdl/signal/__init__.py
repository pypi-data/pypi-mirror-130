from pyhgl.hdl._hdl import *
from .Logic import *
from .SInt import *
from .UInt import *


__hdl_op__['__and__'].default = AND
__hdl_op__['__or__'].default = OR
__hdl_op__['__xor__'].default = XOR


# __hdl_op__['__and__'].register(Logic, AND, Logic, SInt, UInt, order='both')
# __hdl_op__['__and__'].register(SInt, AND, Logic, SInt, UInt, order='both')
# __hdl_op__['__and__'].register(UInt, AND, Logic, SInt, UInt, order='both')

# __hdl_op__['__or__'].register(Logic, OR, Logic, SInt, UInt, order='both')
# __hdl_op__['__or__'].register(SInt, OR, Logic, SInt, UInt, order='both')
# __hdl_op__['__or__'].register(UInt, OR, Logic, SInt, UInt, order='both')

# __hdl_op__['__xor__'].register(Logic, XOR, Logic, SInt, UInt, order='both')
# __hdl_op__['__xor__'].register(SInt, XOR, Logic, SInt, UInt, order='both')
# __hdl_op__['__xor__'].register(UInt, XOR, Logic, SInt, UInt, order='both')

