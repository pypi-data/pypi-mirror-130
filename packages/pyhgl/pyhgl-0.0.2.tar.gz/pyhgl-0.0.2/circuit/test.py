#pyhdls 0.0.1



from pyhdls.hdl.module import *
from pyhdls import config



config.logger.info("----------------------- Bundle test:")


@bundle 
def AdderIO(width, *args):
    x = y = UInt(1, w=width)
    z = Vec.Full(4, UInt("32'd3"))
    z = Bundle(
        valid = UInt(True),
        ready = UInt(False)
    )
    return locals() 

c = AdderIO(8)
print(c)


@enum 
class state:
    idle = read = write1 = write2 = ... 
    
print(state)


config.logger.info("----------------------- Module test:")


def mylogic(sel, a, b) -> Signal:
    ret = Wire(a)
    with When(sel):
        ret <<= b 
    return ret


class mymodule(Module):
    def __init__(self, width):
        super().__init__()
        io = IO(Bundle(
            a = Input(UInt("4'b0010")),
            b = Input(UInt("4'b0100")),
            c = Output(UInt("8'b1111")) 
        ))
        x = Wire(io.a | io.b)  # 0110
        y = Wire( ~(x & "4'b0111")) # 1001
        z = Mux(UInt("2'b1"), x, y) # 0110
        m = Slice(y, 3, 1)      # 100
        n = Cat(UInt(1),z,m)    # 10110100
        c_next = Reg(~n, init=UInt("8'h0"))
        c_next_next = Reg(c_next, init=UInt("8'haa"))
        io.c <<= c_next_next        # 01001011
        

        
        when(io.a):
            c_next <<= c_next_next
        
        when io.b:
            when(c_next):
                io.c <<= "8'hff"
            otherwise:
                io.c <<= mylogic(c_next, n, c_next_next)
        
        
        super().__post__()

m = mymodule(8)
c = Circuit(m)

c.show()

for i in range(6):
    print('-----------------')
    c.step()
    print(m.c_next,end='')
    print(m.c_next_next,end='')
    print(m.io.c)


from pyhdls.parser import * 

src="""#pyhdls
when a.c:
    ...
"""

# for i in _tokenize(src):
#     print(i)
    
tree = hdl_parse(src,"aaa")

print(ast_dump(tree))
# compile(tree, "aaa", 'exec')

import ast 
ast.With()
