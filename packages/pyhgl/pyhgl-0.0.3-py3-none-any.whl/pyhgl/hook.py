""" 
python import hook: https://www.python.org/dev/peps/pep-0302/
reference: https://github.com/pfalcon/python-imphook
"""

import importlib
import sys 
import traceback

from pyhgl.parser import hdl_compile
from pyhgl import config



_hdlext = '.pyh'


class HdlFileLoader(importlib._bootstrap_external.FileLoader):

    def create_module(self, spec):
        # print(spec.name, spec.origin)
        # print(self.name, self.path)

        with open(self.path) as f:
            source_code = f.read()
        self.code_obj = hdl_compile(source_code, self.path)
        
        return None
        
    def exec_module(self, module):
        try:
            exec(self.code_obj, module.__dict__)  
        except:
            print(traceback.format_exc())

def add_import_hook():

    for i, path_hook in enumerate(sys.path_hooks):
        if not isinstance(path_hook, type):
            # Assume it's a type wrapped in a closure,
            # as is the case for FileFinder.
            path_hook = type(path_hook("."))
        if path_hook is importlib._bootstrap_external.FileFinder:
            sys.path_hooks.pop(i)
            insert_pos = i
            break
    else:
        config.logger.warning("Could not find existing FileFinder to replace, installing ours as the first to use")
        insert_pos = 0

    # Mirrors what's done by importlib._bootstrap_external._install(importlib._bootstrap)
    # loaders for different file extensions
    loaders = [(HdlFileLoader, [_hdlext])] + importlib._bootstrap_external._get_supported_file_loaders()
    # path_hook closure captures supported_loaders in itself, return FileFinder
    sys.path_hooks.insert(insert_pos, importlib._bootstrap_external.FileFinder.path_hook(*loaders))
    sys.path_importer_cache.clear()

add_import_hook() 



