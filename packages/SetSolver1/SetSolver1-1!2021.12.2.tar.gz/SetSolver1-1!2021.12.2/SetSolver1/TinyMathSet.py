#!/usr/bin/env python3
# coding: utf-8

class TinyMathSet(frozenset):
    _total_deep_len = None

    def __repr__(self):
        if self == frozenset():
            return "{}"
        return str(set(self))

    def deep_len(self):
        return sum(el.deep_len() if isinstance(el, TinyMathSet) else 1 for el in self)

    def total_deep_len(self):
        if self._total_deep_len is None:
            self._total_deep_len = sum(el.total_deep_len()+1 if isinstance(el, TinyMathSet) else 1 for el in self)
        return self._total_deep_len
