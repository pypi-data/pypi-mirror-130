from typing import Any, Dict, List, Optional, Tuple, Union

import re 
import math

def width_infer(a: int, signed = False)->int:
    ''' 
    signed = False:
        a >= 0: uint 
        a < 0 : sint 
    signed = True:
        a : sint
    '''
    if a < 0:
        return math.ceil(math.log2(-a)) + 1   
    else:
        width_uint = 1 if a < 2 else math.floor(math.log2(a)) + 1
        if not signed:
            return width_uint
        else:
            return 1 if a == 0 else width_uint + 1
        return width_uint + int(signed)



def str2int(a:str, signed = False)->tuple:
    ''' 
    $1111_0000  signed 2's comp, store as is 
    +8'hf       signed, width = 8
    -8'hff      error, overflow
    '''
    a = a.lower()
    if a[0] == '$':
        value, width = str2uint(a[1:])   
        if value >> (width-1):   # sign ext
            value |=  -(1<<width)
        return (value, width, True)
    elif a[0] in ['+','-']:
        value, width = str2uint(a[1:])
        value = value if a[0] == '+' else -value 
        required_width = width_infer(value, signed = True)
        if "'" in a :    # width defined but overflow
            assert width >= required_width, "overflow"
        else:
            width = required_width
        return (value, width, True)
    elif signed:  
        return str2int('+' + a)
    else:       # unsigned
        value, width = str2uint(a)
        return (value, width, False)

def str2uint(a:str)->tuple:
    """ 
    input:
        1111_0000   unsigned bin 
        b1111_0000  unsigned bin 
        8'b11       unsigned bin
            
        h12ab       unsigned hex 
        8'hff       unsigned hex 
        
        d123        dec 
        8'd123      dec
        
    return:
        (value, width)
    """
    a_ = a
    a = a.lower()
    width = None
    if r := re.match(r"(\d+)'(.+)", a):
        width = int(r.groups()[0])
        a = r.groups()[1] 
    if a[0] == 'd':
        a = re.sub(r'[^0-9]', '',a) 
        value = int(a)
        width = width if width is not None else width_infer(value)
    elif a[0] == 'h':
        a = re.sub(r'[^0-9a-f]', '',a)
        width = width if width is not None else len(a)*4
        value = int(a, 16)
    else:
        a = re.sub(r'[^01]', '',a)
        width = width if width is not None else len(a)
        value = int(a, 2)
        
    required_width = width_infer(value)
    assert required_width <= width, f'overflow:{a_}'
    return value, width


def int2str(value: int, width: int) -> str:
    return ('{:0>'+str(width)+'b}').format(value & ( (1 << width) - 1))