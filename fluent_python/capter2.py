#!/usr/bin/env python3
# -*_ coding: utf8 -*-

from math import hypot


class Vector:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __repr__(self):
        return 'Vector({}, {})'.format(self._x, self._y)

    def __str__(self):
        return 'hahahha'

    def __abs__(self):
        return hypot(self._x, self._y)

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self._x + other._x
        y = self._y + other._y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self._x * scalar, self._y * scalar)


if __name__ == '__main__':
    print(Vector(3, 4))
