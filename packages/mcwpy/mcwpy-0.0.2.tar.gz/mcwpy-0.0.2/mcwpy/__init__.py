# -*- coding: utf-8 -*-
""" MCWPy - Minecraft With Python

MCWPy is a Python library for creating Minecraft datapacks using Python.
    https://github.com/vianneyveremme/minecraft_with_python
"""
import sys
import warnings


# Checking Python version (should be above 3.9.5)
if sys.version_info < (3, 9, 5):
    warnings.warn("For optimal results it is recommended to use Python 3.9.5 or above.", RuntimeWarning)
