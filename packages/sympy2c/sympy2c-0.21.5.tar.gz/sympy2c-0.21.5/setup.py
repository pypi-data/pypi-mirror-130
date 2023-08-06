#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["sympy<1.4", "numpy", "Cython>=0.29.24", "requests"]


setup(
    version="0.21.5",  # changing version number here is sufficient!
    author="Uwe Schmitt",
    author_email="uwe.schmitt@id.ethz.ch",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description=(
        "sympy2c is a sympy to c compiler including solving odes at c level."
    ),
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="sympy2c",
    name="sympy2c",
    packages=find_packages("src"),
    package_dir={"": "src"},
    test_suite="tests",
    zip_safe=False,
)
