

from .hdl_tokenizer import _tokenize as hdl_tokenize
from .hdl_parser import HdlParser, Tokenizer
from ast import *

__all__ = ['hdl_tokenize', 'hdl_parse', 'hdl_compile', 'ast_dump']

def wrapped_tokenizer(source:str, verbose:bool = False) -> Tokenizer:

    # FIXME preprocess

    return Tokenizer(hdl_tokenize(source), verbose=verbose)


def hdl_parse(source:str, filename="<string>", py_version = None, verbose = False):
    tokenizer = wrapped_tokenizer(source)
    ast_tree = HdlParser(tokenizer, verbose=verbose, filename = filename, py_version=py_version).parse()
    return ast_tree

def hdl_compile(source:str, filename:str):
    
    ast_tree = hdl_parse(source, filename) 
    # FIXME postprocess
    code_obj = compile(ast_tree, filename, 'exec') 
    
    return code_obj






# see https://bitbucket.org/takluyver/greentreesnakes/src/master/astpp.py
def ast_dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.
    """
    def _format(node, level=0):
        if isinstance(node, AST):
            fields = [(a, _format(b, level)) for a, b in iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)

    if not isinstance(node, AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)
