import glob
import inspect
import os
import shutil
import sys
from pathlib import Path

cwd = Path(__file__).parent
dlls = cwd / 'DLLs' 
dll = 'WinAutoGui.dll'
namespace = 'WinAutoGui'
class_name = 'WinAutoGui'
build_dir = cwd / 'src' / 'WinAutoGuiLib' / 'build'
publish_dir = cwd / 'src' / 'WinAutoGuiLib' / 'publish'

from clr_loader import get_coreclr
from pythonnet import set_runtime
rt = get_coreclr(runtime_config = str(publish_dir / 'WinAutoGui.runtimeconfig.json'))
set_runtime(rt)

import clr

from System.Reflection import Assembly # type: ignore
from System.IO import File # type: ignore
from System import Activator


def copy_dlls():
    try:
        if dlls.exists(): shutil.rmtree(dlls)
        os.mkdir(dlls)
        for assembly in glob.glob(str(publish_dir) + "/*.dll"):
            if not assembly.endswith(dll):
                shutil.copy(assembly, dlls)

        shutil.copy(publish_dir / dll, cwd)
    except:
        pass

def update_dll():
    if build_dir.exists():
        shutil.copy(build_dir / dll, cwd)

def rename_stubs():
    stubs_pyi = cwd / 'typings' / namespace / '__init__.pyi'
    stubs_py = cwd / 'typings' / namespace / '__init__.py'

    if stubs_pyi.exists():
        if stubs_py.exists(): os.remove(stubs_py)
        shutil.copy(stubs_pyi, stubs_py)

def get_functions(clazz):
    functions = inspect.getmembers(clazz, predicate=inspect.isfunction)
    return {
        fn_name: fn
        for fn_name, fn in functions 
        if not fn_name.startswith('__')
    }

def load_libraries(dir: str):
    sys.path.append(dir)
    
    for dll in glob.glob(dir + "/*.dll"):
        clr.AddReference(Path(dll).stem) # type: ignore

def get_class(assembly):
    obj_type = assembly.GetType(namespace + '.' + class_name)
    return Activator.CreateInstance(obj_type)

def get_class_stub():
    from typings.WinAutoGui import WinAutoGui as WinAutoGuiStub
    return WinAutoGuiStub

class PyWinAutoGui:
    def __init__(self):
        copy_dlls()
        load_libraries(str(dlls))
        self.init()

    def init(self):
        update_dll()
        rename_stubs()
        assembly = Assembly.Load(File.ReadAllBytes(str(cwd / dll)))
        self.library = get_class(assembly)
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
