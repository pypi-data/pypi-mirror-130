#!/usr/bin/env python
# coding=UTF-8

"""
key-pressing

Detect key pressing in Python.
"""

from sys import version
if "G" in version :
    from key_pressing.posix import *
else :
    from key_pressing.win import *
del version
