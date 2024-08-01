import glob
import inspect
import os
import shutil
from pathlib import Path

import clr
from System.Reflection import Assembly # type: ignore
from System.IO import File # type: ignore
from System import Activator

cwd = Path(__file__).parent
dlls = cwd / 'DLLs' 
dll = 'WinAutoGui.dll'
namespace = 'WinAutoGui'
class_name = 'WinAutoGui'

def copy_dlls():
    if dlls.exists(): shutil.rmtree(dlls)
    shutil.copytree(cwd / 'src' / 'WinAutoGuiLib' / 'publish', dlls)

def update_dll():
    shutil.copy(cwd / 'src' / 'WinAutoGuiLib' / 'build' / dll, dlls)

def rename_stubs():
    stubs_pyi = cwd / 'typings' / namespace / '__init__.pyi'
    stubs_py = cwd / 'typings' / namespace / '__init__.py'

    if stubs_pyi.exists():
        if stubs_py.exists(): os.remove(stubs_py)
        os.rename(stubs_pyi, stubs_py)

def get_functions(clazz):
    functions = inspect.getmembers(clazz, predicate=inspect.isfunction)
    return {
        fn_name: fn
        for fn_name, fn in functions 
        if not fn_name.startswith('__')
    }

def load_libraries(dir: str):
    return {
        Path(dll).name: Assembly.Load(File.ReadAllBytes(str(dll)))
        for dll in glob.glob(dir + "/*.dll")
    }

def get_class(assembly):
    obj_type = assembly.GetType(namespace + '.' + class_name)
    return Activator.CreateInstance(obj_type)

def get_class_stub():
    from typings.WinAutoGui import WinAutoGui as WinAutoGuiStub
    return WinAutoGuiStub

class PyWinAutoGui:
    def __init__(self):
        copy_dlls()
        self.init()

    def init(self):
        update_dll()
        rename_stubs()
        libs = load_libraries(str(dlls))
        self.library = get_class(libs.get(dll))
        self.lib_stub = get_class_stub()

    def get_keyword_arguments(self, name):
        if name == 'r':
            return []

        func = get_functions(self.lib_stub).get(name)
        _, *args = inspect.getfullargspec(func).args
        return args

    def get_keyword_names(self):
        return ['r'] + list(get_functions(self.lib_stub).keys())

    def run_keyword(self, name: str, args, kwargs):
        if name == 'r':
            return self.init()
        
        return getattr(self.library, name)(*args, **kwargs)
