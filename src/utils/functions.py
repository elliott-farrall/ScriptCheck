import os
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from types import FunctionType
from typing import Any, cast
from warnings import catch_warnings, simplefilter

def pass_by_value(func: FunctionType) -> FunctionType:
    def wrapper(*args) -> Any:
        args_copy = [deepcopy(arg) for arg in args]
        return func(*args_copy)
    return cast(FunctionType, wrapper)

def safe_evaluate(func: FunctionType, *args) -> Any:
    with open(os.devnull, 'w') as devnull, redirect_stdout(devnull), redirect_stderr(devnull), catch_warnings():
        simplefilter("ignore")
        return pass_by_value(func)(*args)
