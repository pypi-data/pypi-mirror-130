#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations

from itertools import chain, combinations
from SetSolver1.MathSet import MathSet
from SetSolver1.MODE import MODE, GET_BY_KEY, CONST_WAY, RESULT
from SetSolver1.TinyMathSet import TinyMathSet
from SetSolver1.helper.BaseTypes import ConstDictType, ResultType
from SetSolver1.helper.update import to_tiny_math_set


class SimpleMathSet(MathSet):
    """
    Class SimpleMathSet, inherit by 'BaseSet'
    """
    value: frozenset[TinyMathSet | tuple | int | str]
    way: tuple[MODE, (SimpleMathSet | None), (SimpleMathSet | None)]

    def __init__(self, value, way):
        """
        init SimpleMathSet
        :type value: frozenset[TinyMathSet | tuple | int | str] | collections.abc.Iterable[
        TinyMathSet | tuple | int | str]
        :type way: (MODE, SimpleMathSet | None, SimpleMathSet | None)
        """
        if type(value) != frozenset:
            value = frozenset(value)
        super().__init__(value, way)

    def __str__(self):
        if self.is_empty():
            return "{}"
        return str(set(self.value))

    def is_empty(self):
        """
        Is SimpleMathSet empty?
        :rtype: bool
        """
        return self.value == frozenset()

    def union(self, y):
        """
        German: Vereinigungsmenge
        :type y: SimpleMathSet
        :rtype: SimpleMathSet
        """
        # self.value.union(y.value) # TODO ist faster?
        copy = set(self.value)
        copy.update(y.value)
        return SimpleMathSet(copy, (GET_BY_KEY[self.union.__name__], self, y))

    def complement(self, y):
        """
        German: Komplement - Subtraktion von Mengen
        :type y: SimpleMathSet
        :rtype: SimpleMathSet
        """
        return SimpleMathSet(self.value.difference(y.value), (GET_BY_KEY[self.complement.__name__], self, y))

    def intersection(self, y):
        """
        German: Schnittmenge
        :type y: SimpleMathSet
        :rtype: SimpleMathSet
        """
        return SimpleMathSet(self.value.intersection(y.value), (GET_BY_KEY[self.intersection.__name__], self, y))

    def power_set(self):
        """
        German: Potenzmenge
        :rtype: SimpleMathSet
        """
        return SimpleMathSet(
            [TinyMathSet(y) for y in chain.from_iterable(
                combinations(self.value, i) for i in range(len(self) + 1))],
            (GET_BY_KEY[self.power_set.__name__], self, None))

    def symmetric_difference(self, y):
        """
        German: Symmetrische Differenz
        :type y: SimpleMathSet
        :rtype: SimpleMathSet
        """
        return SimpleMathSet(self.value.symmetric_difference(y.value),
                             (GET_BY_KEY[self.symmetric_difference.__name__], self, y))


class SimpleMathSetConstDictType(ConstDictType):
    def __init__(self, data):
        """
        :type data: dict[str, set[frozenset | int] | str]
        :raises ValueError:
        """
        _const = dict()
        for letter in data.keys():
            if type(data[letter]) == str:
                from ast import literal_eval
                _const[letter] = SimpleMathSet(to_tiny_math_set(
                    literal_eval(data[letter].replace("{", "[").replace("}", "]"))
                ), CONST_WAY)
            else:
                # _const[letter] = SimpleMathSet(data[letter], CONST_WAY)
                _const[letter] = SimpleMathSet(to_tiny_math_set(data[letter]), CONST_WAY)
            _const[letter].correct_way()
        super().__init__(_const)


class SimpleMathSetResultType(ResultType):
    _result: SimpleMathSet

    def __init__(self, data):
        """
        :type data: set[frozenset | int] | str
        """
        if type(data) == str:
            from ast import literal_eval
            super().__init__(SimpleMathSet(
                to_tiny_math_set(literal_eval(data.replace("{", "[").replace("}", "]"))),
                RESULT))
        else:
            super().__init__(SimpleMathSet(to_tiny_math_set(data), RESULT))
