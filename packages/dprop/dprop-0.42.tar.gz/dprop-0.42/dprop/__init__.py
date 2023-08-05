#  Copyright 2021 Kosio Karchev
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.

from __future__ import annotations

from typing import Any, Callable, Generic, Type, TypeVar, Union
from warnings import warn

import attr


__version__ = '0.42'


_T = TypeVar('_T')


@attr.s(auto_attribs=True, init=False, repr=False, hash=False)
class BaseDProp(property, Generic[_T]):
    owner: Type[_T] = attr.ib(init=False)
    name: str = attr.ib(init=False)
    value_name: str = attr.ib(init=False)

    dependents: set[BaseDProp] = attr.Factory(set)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # noinspection PyUnresolvedReferences
        self.__attrs_init__()

    def __repr__(self):
        return f'<{self.owner.__name__}.{self.name}>'

    def get_value_name(self):
        return f'_{self.name}_value'

    def __set_name__(self, owner: Type[_T], name: str):
        self.owner = owner
        self.name = name
        self.value_name = self.get_value_name()

    def invalidate(self, instance: _T):
        self.invalidate_deps(instance)

    def invalidate_deps(self, instance: _T):
        for dep in self.dependents:
            dep.invalidate(instance)


class idprop(BaseDProp[_T], Generic[_T]):
    # noinspection PyMethodOverriding
    def __get__(self, instance, owner):
        try:
            return getattr(instance, self.value_name) if instance is not None else self
        except AttributeError:
            raise AttributeError(f'Independent property {self} has not been set.') from None

    def __set__(self, instance, value):
        setattr(instance, self.value_name, value)
        self.invalidate_deps(instance)

    def __delete__(self, instance):
        delattr(instance, self.value_name)
        self.invalidate_deps(instance)


@attr.s(auto_attribs=True, init=False, repr=False, hash=False)
class dprop(BaseDProp):
    @attr.s(auto_attribs=True, slots=True)
    class DPropValue(Generic[_T]):
        value: _T = None
        valid: bool = False

        def set_value(self, val):
            self.value = val
            self.valid = True

    dependencies: set[BaseDProp] = attr.Factory(set)

    def get_value(self, instance: _T) -> DPropValue:
        if (val := getattr(instance, self.value_name, None)) is None:
            val = self.DPropValue()
            setattr(instance, self.value_name, val)
        return val

    # noinspection PyMethodOverriding
    def __get__(self, instance: _T, owner: Type[_T]):
        if instance is None:
            return self

        if not (val := self.get_value(instance)).valid:
            val.set_value(super().__get__(instance, owner))
            val.valid = True
        return val.value

    def __set__(self, instance: _T, value):
        if self.dependencies:
            warn(f'Setting a value on {self},'
                 f'which depends on {self.dependencies}.',
                 RuntimeWarning)

        self.get_value(instance).set_value(value)
        self.invalidate_deps(instance)

    def invalidate(self, instance: _T):
        self.get_value(instance).valid = False
        super().invalidate(instance)

    def depends_on(self, *dprops):
        self.dependencies.update(dprops)
        for p in dprops:
            p.dependents.add(self)
        return self


def depends_on(*dprops: BaseDProp) -> Callable[[...], dprop]:
    def _f(func):
        return dprop(func).depends_on(*dprops)
    return _f


def independent(_t: Type[_T] = Any) -> Union[_T, idprop]:
    return idprop()
