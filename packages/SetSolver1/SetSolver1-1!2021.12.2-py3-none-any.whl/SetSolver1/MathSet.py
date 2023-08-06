#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations

from SetSolver1.MODE import MODE, TEMPORARY_CREATED, CONST, CONST_WAY
from SetSolver1.TinyMathSet import TinyMathSet


class MathSet:
    """
    BaseClass BaseSet
    """
    def __init__(self, value, way):
        """
        Constructor method
        :type value: any
        :type way: (MODE, any, any)
        """
        self.value = value
        self.way = way

    def __repr__(self):
        return "{0}({1})".format(type(self).__name__, self.__dict__)

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        # Default: hash(x)==id(x)/16
        # https://stackoverflow.com/a/11324771
        # https://docs.python.org/3/glossary.html#term-hashable
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        print("NotImplemented Equality Compare")
        return NotImplemented

    def __len__(self):
        """
        :rtype: int
        """
        return len(self.value)

    def correct_way(self):
        """
        Helper method to set correct way to consts
        """
        if self.way == CONST_WAY:
            self.way = (CONST, self, None)

    def walk_way(self, going_by=None):
        """
        Walk through the way and count steps
        :param going_by: value adding per step of way
        :type going_by: int
        :raises ValueError:
        :return: steps of way
        :rtype: int
        """
        mode = self.way[0]
        if mode == TEMPORARY_CREATED:
            raise ValueError("MODE.TEMPORARY_CREATED not allowed here")
        if mode == CONST:
            return 0
        lt = list()
        for i in mode[0]:
            if self.way[i] is not None:
                lt.append(self.way[i].walk_way(going_by))
        return sum(lt) + (going_by if going_by is not None else mode[1])

    def sort_key(self):
        """
        ascending order so: 2 is before 5
        :rtype: (int, int)
        """
        # TODO ist there a way to sort by second key only if needed?
        return self.walk_way(going_by=1), self.walk_way()

    def deep_len(self):
        return sum(el.deep_len() if type(el) == TinyMathSet else 1 for el in self.value)

    def total_deep_len(self):
        return sum(el.total_deep_len()+1 if type(el) == TinyMathSet else 1 for el in self.value)

    def is_empty(self):
        """
        Is MathSet empty?
        :rtype: bool
        """
        return len(self.value) == 0

    def union(self, y):
        raise RuntimeError("this operation is not allowed")

    def complement(self, y):
        raise RuntimeError("this operation is not allowed")

    def intersection(self, y):
        raise RuntimeError("this operation is not allowed")

    def power_set(self):
        raise RuntimeError("this operation is not allowed")

    def symmetric_difference(self, y):
        raise RuntimeError("this operation is not allowed")

    def composition(self, y):
        raise RuntimeError("this operation is not allowed")

    def converse_relation(self):
        raise RuntimeError("this operation is not allowed")

    def reflexive_closure(self):
        raise RuntimeError("this operation is not allowed")

    def transitive_closure(self):
        raise RuntimeError("this operation is not allowed")

    def disjoint_union(self, y):
        raise RuntimeError("this operation is not allowed")

    def multi_set_difference(self, y):
        raise RuntimeError("this operation is not allowed")
