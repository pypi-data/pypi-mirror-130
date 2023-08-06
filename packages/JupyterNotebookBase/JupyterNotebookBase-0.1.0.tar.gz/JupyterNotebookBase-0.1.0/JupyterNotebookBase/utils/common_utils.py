# -*- coding:utf-8 -*-
from notebook._version import __version__


def is_new_notebook():
    res = False
    try:
        res = __version__ >= "6,4,0"
    except:
        pass
    return res
