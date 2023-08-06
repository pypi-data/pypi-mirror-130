#!/usr/bin/env python3
# coding: utf-8


class MODE:
    _value: tuple[tuple[int], int, int]
    _print_str: str

    def __init__(self, used_vars, priority, is_commutative, print_str):
        """
        Constructor method
        :type used_vars: tuple[int]
        :type priority: int
        :type is_commutative: int
        :type print_str: str
        """
        self._value = (used_vars, priority, is_commutative)
        self._print_str = print_str

    def __getitem__(self, item):
        """
        __getitem__ method
        :type item: int
        :rtype: int | tuple
        """
        return self._value[item]

    def __lt__(self, other):
        if type(other) == self.__class__:
            return self[1] < other[1]

    def __repr__(self):
        return list(GET_BY_KEY.keys())[list(GET_BY_KEY.values()).index(self)]

    def format(self, x, y):
        """
        returns format _print_str with x and y
        :type x: str
        :type y: str
        :rtype: str
        """
        return self._print_str.format(x=x, y=y)

    def is_multi_mode(self):
        return self[0] == (1, 2)

    def is_single_mode(self):
        return not self.is_multi_mode()


CONST = MODE(
    used_vars=tuple(),
    priority=1,
    is_commutative=1,
    print_str='{x}'
)
IDENTITY = MODE(
    used_vars=tuple(),
    priority=1,
    is_commutative=1,
    print_str=''
)
TEMPORARY_CREATED = MODE(
    used_vars=tuple(),
    priority=1,
    is_commutative=1,
    print_str=''
)
UNION = MODE(
    used_vars=(1, 2),
    priority=1,
    is_commutative=1,
    print_str='({x}+{y})'
)
COMPLEMENT = MODE(
    used_vars=(1, 2),
    priority=1,
    is_commutative=0,
    print_str='({x}-{y})'
)
INTERSECTION = MODE(
    used_vars=(1, 2),
    priority=2,
    is_commutative=1,
    print_str='({x}&{y})'
)
COMPOSITION = MODE(
    used_vars=(1, 2),
    priority=3,
    is_commutative=0,
    print_str='({x}.{y})'
)
POWER_SET = MODE(
    used_vars=(1,),
    priority=4,
    is_commutative=1,
    print_str='pow({x})'
)
SYMMETRIC_DIFFERENCE = MODE(
    used_vars=(1, 2),
    priority=99,  # TODO
    is_commutative=1,
    print_str='({x}sym{y})'
)
CONVERSE_RELATION = MODE(
    used_vars=(1,),
    priority=3,
    is_commutative=1,
    print_str='inverse({x})'
)
REFLEXIVE_CLOSURE = MODE(
    used_vars=(1,),
    priority=2,
    is_commutative=1,
    print_str='reflexive_cl({x})'
)
TRANSITIVE_CLOSURE = MODE(
    used_vars=(1,),
    priority=2,
    is_commutative=1,
    print_str='transitive_cl({x})'
)
MULTISET_DISJOINT_UNION = MODE(
    used_vars=(1, 2),
    priority=2,
    is_commutative=1,
    print_str='({x}+{y})'
)
MULTISET_DIFFERENCE = MODE(
    used_vars=(1, 2),
    priority=2,
    is_commutative=0,
    print_str='({x}-{y})'
)

GET_BY_KEY = {
    "CONST":                CONST,
    "IDENTITY":             IDENTITY,
    "TEMPORARY_CREATED":    TEMPORARY_CREATED,
    "union":                UNION,
    "complement":           COMPLEMENT,
    "intersection":         INTERSECTION,
    "composition":          COMPOSITION,
    "power_set":            POWER_SET,
    "symmetric_difference": SYMMETRIC_DIFFERENCE,
    "converse_relation":    CONVERSE_RELATION,
    "reflexive_closure":    REFLEXIVE_CLOSURE,
    "transitive_closure":   TRANSITIVE_CLOSURE,
    "disjoint_union":       MULTISET_DISJOINT_UNION,
    "multi_set_difference": MULTISET_DIFFERENCE
}

CHOOSE_BY_INDEX = [UNION, COMPLEMENT, INTERSECTION, COMPOSITION, POWER_SET, CONVERSE_RELATION, REFLEXIVE_CLOSURE,
                   TRANSITIVE_CLOSURE, MULTISET_DISJOINT_UNION, MULTISET_DIFFERENCE]
SORTED_CHOOSE_BY_INDEX = sorted(CHOOSE_BY_INDEX)

DEFAULT_NOT_ALLOWED = [COMPOSITION, CONVERSE_RELATION, REFLEXIVE_CLOSURE, TRANSITIVE_CLOSURE, MULTISET_DISJOINT_UNION,
                       MULTISET_DIFFERENCE]
NOT_ALLOWED_EVERYTHING = CHOOSE_BY_INDEX

RESULT = TEMPORARY_CREATED
TEMPORARY_CREATED_WAY = (TEMPORARY_CREATED, None, None)
CONST_WAY = (CONST, None, None)
IDENTITY_WAY = (IDENTITY, None, None)
