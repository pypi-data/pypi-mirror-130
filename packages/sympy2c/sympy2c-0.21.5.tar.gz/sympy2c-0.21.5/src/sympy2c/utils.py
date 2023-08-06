#! /usr/bin/env python
# encoding: utf-8


import functools
import hashlib
import os
import sys
import time
from contextlib import contextmanager

from sympy import Symbol

from .version import __version__


def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except IOError:
            # might be triggered due to race conditin
            assert os.path.exists(folder)


def align(text):
    """removes | markers and everyting left to them"""
    lines = text.split("\n") + ["", ""]
    return "\n".join(line.partition("|")[2] for line in lines)


def concat_generator_results(function):
    """code generator methods here *yield* code blocks.
    This decorator then *returns* the concatendated blocks
    as a single string
    """

    @functools.wraps(function)
    def inner(*a, **kw):
        concat = "\n".join(function(*a, **kw))
        stripped = [line.rstrip() for line in concat.split("\n")]
        return "\n".join(stripped)

    return inner


def bound_symbols(*expressions):
    def union(generator):
        return set.union(*list(generator))

    all_symbols = union(expression.atoms(Symbol) for expression in expressions)
    free_symbols = union(expression.free_symbols for expression in expressions)

    return all_symbols - free_symbols


@contextmanager
def run_in_folder(folder):
    create_folder_if_not_exists(folder)
    current_folder = os.getcwd()
    try:
        os.chdir(folder)
        yield
    finally:
        os.chdir(current_folder)


@contextmanager
def timeit(task):
    print("start", task)
    started = time.time()
    yield
    print("time needed for {}: {:.2f} seconds".format(task, time.time() - started))


PRINT_INFO = os.environ.get("PRINTHASHES") is not None


class Hasher:
    def __init__(self):
        self._hasher = hashlib.md5()

    def update(self, name, what):
        self._hasher.update(what.encode("utf-8"))
        if PRINT_INFO:
            print("HASH", name, self._hasher.hexdigest(), what)

    def hexdigest(self):
        return self._hasher.hexdigest()[:8]


def base_cache_folder():
    home = os.path.expanduser("~")
    if sys.platform.startswith("darwin"):
        base_folder = os.path.join(home, "Library", "Cache")
    else:
        base_folder = os.path.join(home, "_cache")
    return base_folder


def sympy2c_cache_folder():
    fake_folder = os.environ.get("FAKE_CACHE_FOLDER")
    if fake_folder is not None:
        return fake_folder
    import numpy

    numpy_version = "_".join(numpy.__version__.split("."))
    sympy_version = "_".join(map(str, __version__))
    return os.path.join(
        base_cache_folder(), "sympy2c", sympy_version + "__np_" + numpy_version
    )
