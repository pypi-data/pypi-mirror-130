#! /usr/bin/env python
# encoding: utf-8


import glob
import os
import shutil
import subprocess
from distutils import ccompiler

from .utils import base_cache_folder, create_folder_if_not_exists, run_in_folder

CC = ccompiler.new_compiler().executables["compiler"][0]
HERE = os.path.dirname(os.path.abspath(__file__))


def compile_if_needed(target_folder):

    lsoda_out = os.path.join(target_folder, "lsoda.a")
    if not os.path.exists(lsoda_out):
        with run_in_folder(target_folder):
            for p in glob.glob(os.path.join(HERE, "lsoda_modified", "*.[ch]")):
                shutil.copy(p, ".")

            c_files = glob.glob("*.c")

            output = subprocess.check_output(
                [
                    CC,
                    "-O3",
                    "-c",
                    "-fPIC",
                    "-DINTEGER_STAR_8=1",
                    "-w",
                    "-Wfatal-errors",
                ]
                + c_files,
                shell=False,
                universal_newlines=True,
            )
            print(output)
            o_files = glob.glob("*.o")
            output = subprocess.check_output(
                [
                    "ar",
                    "rcs",
                    lsoda_out,
                ]
                + o_files,
                shell=False,
                universal_newlines=True,
            )
            print(output)
    return lsoda_out


def install_lsoda_fast_if_needed(lsoda_root_folder=None):
    if lsoda_root_folder is None:
        lsoda_root_folder = os.path.join(base_cache_folder(), "sympy2c")

    target_folder = os.path.join(lsoda_root_folder, "lsoda_fast")
    create_folder_if_not_exists(target_folder)
    object_file = compile_if_needed(target_folder)
    return object_file
