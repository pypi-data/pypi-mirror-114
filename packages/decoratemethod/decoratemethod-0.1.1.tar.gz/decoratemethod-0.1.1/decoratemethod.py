# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Callable, TypeVar
import types
from functools import update_wrapper

class _DecorateMethodDescriptor:
    def __init__(self, func, decorator):
        self._func = func
        self._decorator = decorator
        self._name = '_boundmethod_' + func.__name__

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        # for instance, get bound method
        boundmethod = getattr(obj, self._name, None)
        if boundmethod is None:
            boundmethod = types.MethodType(self._func, obj)
            boundmethod = self._decorator(boundmethod)
            update_wrapper(boundmethod, self._func)
            setattr(obj, self._name, boundmethod)
        return boundmethod

    def __set__(self, obj, value) -> None:
        raise AttributeError


_T = TypeVar('_T')

def decorate(decorator_func: Callable[..., _T]) -> _T:
    '''
    decorate a method with give function decorator.

    return a data descriptor get the bound method.

    NOTE:
        this will cache the bound method on instance,
        the name of the bound method is the name of method with prefix `_boundmethod_`.
        ensure you known that if you use `__slots__`.

    ### Example

    ``` py
    from functools import lru_cache
    class Foo:
        @decorate(lru_cache)
        def decorated_method(self, x):
            ...
    ```
    '''
    def wrapper(func):
        return _DecorateMethodDescriptor(func, decorator_func)
    return wrapper
