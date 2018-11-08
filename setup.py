#!/usr/bin/env python

from setuptools import setup

setup(
    name = "rascall",
    version = "0.9",
    description = "Molecular Spectra Generator",
    author = "Clara Sousa-Silva",
    author_email = "cssilva@mit.edu",
    test_suite =  "tests",
    license = "All rights reserved",
    packages = ["rascall"],
    include_package_data = True,
    package_dir = {'rascall' : 'rascall'},
    install_requires = [],
)