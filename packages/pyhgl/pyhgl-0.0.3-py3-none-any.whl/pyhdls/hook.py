""" 
python import hook: https://www.python.org/dev/peps/pep-0302/
deal with py file start with "@pyhdls" at import time
"""

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader
import sys 
import traceback

from pyhdls.parser import hdl_compile
from pyhdls import config

class HdlLoader(Loader):
    """ loads a module. 
    """
    def __init__(self, normal_spec, code_obj):
        self.normal_spec = normal_spec 
        self.code_obj = code_obj 
    
    def create_module(self, spec):
        return None                 # a new module with attributes of spec will be created by cpython
    
    def exec_module(self, module):  # XXX
        try:
            exec(self.code_obj, module.__dict__)  
        except:
            print(traceback.format_exc())

    def get_filename(self, fullname):
        return self.normal_spec.loader.get_filename(fullname)
    
    def is_package(self, fullname):
        return self.normal_spec.loader.is_package(fullname)



class HdlFinder(MetaPathFinder):
    """ find a spec   
    """ 
    @classmethod
    def find_spec(cls, fullname, path, target=None):
        """ 
        fullname: module name 
        path:     __path__ of a package
        """
        # find a normal spec, because pyhdls will not effect import logic of python
        normal_spec = None 
        for finder in sys.meta_path:
            if finder is cls: 
                continue 
            if hasattr(finder, 'find_spec'):
                normal_spec = finder.find_spec(fullname, path, target=target)
            if normal_spec is not None:
                print(fullname, finder)
                break
        # return None if cannot get source code (str type)
        if normal_spec is None or normal_spec.origin == 'builtin':
            return None
        try:
            source_code = normal_spec.loader.get_source(fullname)
        except:
            return None
        # return None if not pyhdls code
        if source_code is None or source_code[:7] != "#pyhdls":
            return None

        if config.hook_verbose:
            config.logger.debug(f"import hdl module: {fullname} from path: {path}")
            config.logger.debug(f"file: {normal_spec.origin}")

        # parse code to python code_object, and return a spec that contains HdlLoader
        try:
            code_obj = hdl_compile(source_code, normal_spec.origin)        # XXX
        except:
            print(traceback.format_exc())
            return None
        return spec_from_loader(fullname, HdlLoader(normal_spec, code_obj))
    

sys.meta_path.insert(0,HdlFinder)



