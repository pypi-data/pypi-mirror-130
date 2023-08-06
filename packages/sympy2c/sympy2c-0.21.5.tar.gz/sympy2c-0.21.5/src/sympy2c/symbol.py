#! /usr/bin/env python
# encoding: utf-8


from functools import partial

from sympy import Symbol

"""
patch existing sympy Symbol class by adding some special methods we
need for code generation.
"""


def c_args_decl(self):
    return self


Symbol.c_args_decl = c_args_decl
Symbol.as_function_arg = c_args_decl


def cython_decl(self):
    return "double " + str(self)


Symbol.cython_decl = cython_decl


def _name(self):
    return self.name


Symbol._name = _name

Symbol.is_vector = False


def setter_c_code(self):
    return """extern "C" void _set_{name}(double _v){{ {name} = _v; }}""".format(
        name=self.name
    )


Symbol.setter_c_code = setter_c_code


def getter_c_code(self):
    return """extern "C" double _get_{name}(){{ return {name}; }}""".format(
        name=self.name
    )


Symbol.getter_c_code = getter_c_code


def setter_header_code(self):
    return "void _set_{name}(double _v); ".format(name=self.name)


Symbol.setter_header_code = setter_header_code


def getter_header_code(self):
    return "double _get_{name}(); ".format(name=self.name)


Symbol.getter_header_code = getter_header_code

Symbol.setter_cython_header_code = setter_header_code
Symbol.getter_cython_header_code = getter_header_code


def cython_globals_setter_code(self):
    from .utils import align

    return (
        align(
            """
    |if "{name}" in _g:
    |    if _g["{name}"] is None:
    |       _set_{name}(np.nan)
    |    else:
    |       _set_{name}(<double>_g["{name}"])
    """
        )
        .format(name=self.name)
        .rstrip()
    )


Symbol.cython_globals_setter_code = cython_globals_setter_code


def cython_globals_getter_code(self):
    return """result['{name}'] = _get_{name}()""".format(name=self.name)


Symbol.cython_globals_getter_code = cython_globals_getter_code

Symbol = partial(Symbol, real=True)


def symbols(txt):
    return [Symbol(n) for n in txt.split()]
