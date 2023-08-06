#! /usr/bin/env python
# encoding: utf-8


import abc


class WrapperBase(abc.ABC):
    @abc.abstractmethod
    def c_header(self):
        ...

    @abc.abstractmethod
    def c_code(self, header_file_path):
        ...

    @abc.abstractmethod
    def cython_code(self, header_file_path):
        ...

    @abc.abstractmethod
    def determine_required_extra_wrappers(self):
        ...

    @abc.abstractmethod
    def setup_code_generation(self):
        ...
