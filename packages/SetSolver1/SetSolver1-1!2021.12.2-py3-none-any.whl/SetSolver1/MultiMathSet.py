#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations

from SetSolver1.MathSet import MathSet
from SetSolver1.MODE import MODE, GET_BY_KEY, CONST_WAY, RESULT
from SetSolver1.helper.BaseTypes import ConstDictType, ResultType


class MultiMathSet(MathSet):
    """
    Class MultiMathSet, inherit by 'BaseSet'
    """
    value: dict[str, int]
    way: tuple[MODE, (MultiMathSet | None), (MultiMathSet | None)]

    def __init__(self, value, way):
        """
        Constructor method
        :type value: dict[str, int]
        :type way: (MODE, MultiMathSet | None, MultiMathSet | None)
        """
        super().__init__(value, way)

    def __hash__(self):
        return hash(tuple(sorted(self.value.items())))

    def is_empty(self):
        """
        Is MultiMathSet empty?
        :rtype: bool
        """
        return self.value == dict()

    def total_deep_len(self):
        a = self.value.values()
        return len(a) + sum(a)

    def union(self, y):
        """
        German: Vereinigung
        :type y: MultiMathSet
        :rtype: MultiMathSet
        """
        copy = self.value.copy()
        for y1 in y.value.keys():
            if not y.value[y1] == 0:
                copy[y1] = max(copy.get(y1, 0), y.value[y1])
        return MultiMathSet(copy, (GET_BY_KEY[self.union.__name__], self, y))

    def disjoint_union(self, y):
        """
        German: disjunkte Vereinigung
        :type y: MultiMathSet
        :rtype: MultiMathSet
        """
        copy = self.value.copy()
        for y1 in y.value.keys():
            if not y.value[y1] == 0:
                copy[y1] = copy.get(y1, 0) + y.value[y1]
        return MultiMathSet(copy, (GET_BY_KEY[self.disjoint_union.__name__], self, y))

    def multi_set_difference(self, y):
        """
        German: Differenz
        :type y: MultiMathSet
        :rtype: MultiMathSet
        """

        copy = self.value.copy()
        for y1 in y.value.keys():
            if not y.value[y1] == 0 and y1 in copy.keys() and copy[y1] > y.value[y1]:
                copy[y1] = copy[y1] - y.value[y1]
        return MultiMathSet(copy, (GET_BY_KEY[self.multi_set_difference.__name__], self, y))

    def intersection(self, y):
        """
        German: Schnitt
        :type y: MultiMathSet
        :rtype: MultiMathSet
        """
        copy = self.value.copy()
        for y1 in set(copy.keys()).union(y.value.keys()):
            copy[y1] = min(copy.get(y1, 0), y.value.get(y1, 0))
            if copy[y1] == 0:
                del copy[y1]
        return MultiMathSet(copy, (GET_BY_KEY[self.intersection.__name__], self, y))


class MultiMathSetConstDictType(ConstDictType):
    def __init__(self, data):
        """
        :type data: dict[str, dict[str, int]]
        :raises ValueError:
        """
        _const = dict()
        for letter in data.keys():
            for i in data[letter].values():
                if i < 1:  # check every int is not negative or 0
                    raise ValueError("no negative or zero value allowed in ConstDictType")
            _const[letter] = MultiMathSet(data[letter], CONST_WAY)
            _const[letter].correct_way()
        super().__init__(_const)


class MultiMathSetResultType(ResultType):
    _result: MultiMathSet

    def __init__(self, data):
        """
        :type data: dict[str, int]
        """
        super().__init__(MultiMathSet(data, RESULT))
