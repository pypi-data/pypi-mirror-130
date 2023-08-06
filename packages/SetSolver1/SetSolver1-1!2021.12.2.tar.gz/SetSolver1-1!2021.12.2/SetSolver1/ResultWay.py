#!/usr/bin/env python3
# coding: utf-8

from SetSolver1.MathSet import MathSet
from SetSolver1.helper.BaseTypes import ConstDictType


class ResultWay:
    def __init__(self, result, const_dict, reversed_const_dict, results):
        """
        Constructor method
        :type result: MathSet
        :type const_dict: dict[str, MathSet] | ConstDictType
        :type reversed_const_dict: dict[MathSet, str]
        :type results: set[MathSet]
        """
        self.result = result
        self.const_dict = const_dict
        self.reversed_const_dict = reversed_const_dict
        self.results = results

    def __repr__(self):
        return str(self.result)
