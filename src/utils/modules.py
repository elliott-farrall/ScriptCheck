import os
from contextlib import redirect_stderr, redirect_stdout
from importlib.util import module_from_spec, spec_from_file_location
from types import ModuleType
from warnings import catch_warnings, simplefilter


def import_module(path: str) -> ModuleType | None:
    spec = spec_from_file_location(os.path.basename(path), path)
    if spec is not None:
        module = module_from_spec(spec)
        if spec.loader is not None:
            try:
                with open(os.devnull, 'w') as devnull, redirect_stdout(devnull), redirect_stderr(devnull), catch_warnings():
                    simplefilter("ignore")
                    spec.loader.exec_module(module)
                return module
            except Exception:
                pass
    return None
