#! /usr/bin/env python
# encoding: utf-8


import sympy as sp

# Copyright © 2019 Uwe Schitt <uwe.schmitt@id.ethz.ch>


class Min(sp.Expr):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def free_symbols(self):
        return self.a.free_symbols | self.b.free_symbols

    def to_c(self, visitor):
        return "(_min({}, {}))".format(visitor.visit(self.a), visitor.visit(self.b))


class Max(Min):
    def to_c(self, visitor):
        return "(_max({}, {}))".format(visitor.visit(self.a), visitor.visit(self.b))


class isnan(sp.Expr):
    def __init__(self, a):
        self.a = a

    @property
    def free_symbols(self):
        return self.a.free_symbols

    def to_c(self, visitor):
        # from https://stackoverflow.com/questions/570669
        return "({0} != {0})".format(visitor.visit(self.a))


class hyper_2f1(sp.Expr):
    def __init__(self, a, b, c, x):
        self.a = a
        self.b = b
        self.c = c
        self.x = x

    @property
    def free_symbols(self):
        return (
            self.a.free_symbols
            | self.b.free_symbols
            | self.c.free_symbols
            | self.x.free_symbols
        )

    def to_c(self, visitor):
        # from https://stackoverflow.com/questions/570669
        return "(gsl_sf_hyperg_2F1({}, {}, {}, {}))".format(
            visitor.visit(self.a),
            visitor.visit(self.b),
            visitor.visit(self.c),
            visitor.visit(self.x),
        )
