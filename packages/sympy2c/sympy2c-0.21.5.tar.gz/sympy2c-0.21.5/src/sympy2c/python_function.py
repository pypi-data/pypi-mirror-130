#!/usr/bin/env python

import hashlib
import inspect
from textwrap import dedent
from types import FunctionType

from .wrapper import WrapperBase


class PythonFunction:
    def __init__(self, function):
        assert isinstance(function, FunctionType)
        self.function_src = inspect.getsource(function)
        self.name = function.__name__
        self._unique_id = None

    def get_unique_id(self):
        if self._unique_id is None:
            md5 = hashlib.md5()
            md5.update(self.function_src.encode("utf-8"))
            self._unique_id = md5.hexdigest()
        return self._unique_id

    def wrapper(self):
        return PythonFunctionWrapper(self.name, self.function_src)


class PythonFunctionWrapper(WrapperBase):
    def __init__(self, name, function_src):
        self.name = name
        self.function_src = function_src
        self._unique_id = None

    def c_header(self):
        return ""

    def c_code(self, header_file_path):
        return ""

    def cython_code(self, header_file_path):
        return dedent(self.function_src)

    def determine_required_extra_wrappers(self):
        pass

    def setup_code_generation(self):
        pass

    def get_unique_id(self):
        if self._unique_id is None:
            md5 = hashlib.md5()
            md5.update(self.function_src.encode("utf-8"))
            self._unique_id = md5.hexdigest()
        return self._unique_id
