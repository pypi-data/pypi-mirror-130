#!/usr/bin/env python3
# coding: utf-8

from __future__ import annotations

from SetSolver1.MODE import MODE, GET_BY_KEY, CONST_WAY, RESULT, IDENTITY_WAY
from SetSolver1.SimpleMathSet import SimpleMathSet
from SetSolver1.helper.BaseTypes import ConstDictType, ResultType


class RelationMathSet(SimpleMathSet):
    """
    Class RelationMathSet, inherit by 'BaseSet'
    """
    value: frozenset[tuple[int | str, int | str]]
    identity: RelationMathSet | None
    way: tuple[MODE, (RelationMathSet | None), (RelationMathSet | None)]

    def __init__(self, value, identity, way):
        """
        init RelationMathSet
        :type value: frozenset[(int, int)] | collections.abc.Iterable[(int, int)]
        :type identity: RelationMathSet | None
        :type way: (MODE, RelationMathSet | None, RelationMathSet | None)
        """
        self.identity = identity
        super().__init__(value, way)

    def type_check(self, y):
        """
        Check if the type of MathSets is comparable
        :type y: RelationMathSet
        :raises TypeError:
        """
        if self.identity != y.identity:
            raise TypeError("type_check error")

    def is_identity(self, set_to_identity_of_itself=False):
        """
        :type set_to_identity_of_itself: bool
        :rtype: RelationMathSet | bool
        :raises ValueError:
        """
        if set_to_identity_of_itself:
            if self.identity is not None:
                raise ValueError("It is not allowed to change attribute value of this class")
            self.identity = self
            return self
        else:
            return self.identity == self

    def union(self, y):
        """
        German: Vereinigungsmenge
        :type y: RelationMathSet
        :rtype: RelationMathSet
        """
        self.type_check(y)
        copy = set(self.value)
        copy.update(y.value)
        return RelationMathSet(copy, self.identity, (GET_BY_KEY[self.union.__name__], self, y))

    def complement(self, y):
        """
        German: Komplement - Subtraktion von Mengen
        :type y: RelationMathSet
        :rtype: RelationMathSet
        """
        self.type_check(y)
        return RelationMathSet(self.value.difference(y.value), self.identity,
                               (GET_BY_KEY[self.complement.__name__], self, y))

    def intersection(self, y):
        """
        German: Schnittmenge
        :type y: RelationMathSet
        :rtype: RelationMathSet
        """
        self.type_check(y)
        return RelationMathSet(self.value.intersection(y.value), self.identity,
                               (GET_BY_KEY[self.intersection.__name__], self, y))

    def symmetric_difference(self, y):
        """
        German: Symmetrische Differenz
        :type y: RelationMathSet
        :rtype: RelationMathSet
        """
        self.type_check(y)
        return RelationMathSet(self.value.symmetric_difference(y.value), self.identity,
                               (GET_BY_KEY[self.symmetric_difference.__name__], self, y))

    def composition(self, y):
        """
        TODO optimization
        German: Verkettung
        :type y: RelationMathSet
        :rtype: RelationMathSet
        """
        self.type_check(y)
        lst = list()
        for x1 in self.value:
            for y1 in y.value:
                if x1[1] == y1[0]:
                    lst.append((x1[0], y1[1]))
        return RelationMathSet(lst, self.identity, (GET_BY_KEY[self.composition.__name__], self, y))

    def converse_relation(self):
        """
        TODO optimization
        German: Inverse (Umkehrrelation)
        :rtype: RelationMathSet
        """
        return RelationMathSet(((x1[1], x1[0]) for x1 in self.value), self.identity,
                               (GET_BY_KEY[self.converse_relation.__name__], self, None))

    def reflexive_closure(self):
        """
        TODO optimization
        German: Reflexive Hülle
        :rtype: RelationMathSet
        """
        return RelationMathSet(list(self.value) + [(x3, x3) for x3 in set([x1[x2]
                                                                           for x2 in range(2) for x1 in self.value])],
                               self.identity, (GET_BY_KEY[self.reflexive_closure.__name__], self, None))

    def transitive_closure(self):
        """
        TODO optimization
        German: Transitive Hülle
        :rtype: RelationMathSet
        """
        return RelationMathSet(list(self.value) + [(x1[0], x2[1])
                                                   for x2 in self.value for x1 in self.value if x1[1] == x2[0]],
                               self.identity, (GET_BY_KEY[self.transitive_closure.__name__], self, None))

    def is_reflexive(self):
        """
        :rtype: bool
        """
        if self.identity is None:
            return self.value == self.reflexive_closure().value
        return self.identity.is_subset(self)

    def is_irreflexive(self):
        """
        :rtype: bool
        """
        if self.identity is None:
            """
            One-Line
            return frozenset((x3, x3) for x3 in set([x1[x2] for x2 in range(2) for x1 in self.value])
                             if (x3, x3) in self.value) == frozenset()
            """
            for x1 in self.value:
                if (x1[0], x1[0]) in self.value or (x1[1], x1[1]) in self.value:
                    return False
            return True
        return self.intersection(self.identity).is_empty()

    def is_subset(self, y):
        """
        is_subset
        :type y: RelationMathSet
        :rtype: bool
        """
        # self.value.issubset(y.value)
        self.type_check(y)
        for x1 in self.value:
            if x1 not in y.value:
                return False
        return True

    def is_symmetric_relation(self):
        """
        :rtype: bool
        """
        return self.converse_relation().is_subset(self)

    def is_asymmetric_relation(self):
        """
        :rtype: bool
        """
        return self.intersection(self.converse_relation()).is_empty()

    def is_antisymmetric_relation(self):
        """
        :rtype: bool
        """
        if self.identity is None:
            for x1 in self.value:
                if x1[::-1] in self.value and not x1[0] == x1[1]:
                    return False
            return True
        return self.intersection(self.converse_relation()).is_subset(self.identity)

    def is_transitive(self):
        """
        :rtype: bool
        """
        return self.value == self.transitive_closure().value

    def is_preorder(self):
        """
        German: Quasiordnung
        :return: bool
        """
        return self.is_reflexive() and self.is_transitive()

    def is_equivalence_relation(self):
        """
        German: Äquivalenzrelation (symmetrische Quasiordnung)
        :return: bool
        """
        return self.is_preorder() and self.is_symmetric_relation()

    def is_non_strict_partial_order(self):
        """
        German: Halbordnung (partielle Ordnung)
        :return: bool
        """
        return self.is_reflexive() and self.is_antisymmetric_relation() and self.is_transitive()

    def is_strict_partial_order(self):
        """
        German: Strikte Ordnung
        :return: bool
        """
        return self.is_irreflexive() and self.is_transitive() and self.is_asymmetric_relation()

    def print_properties(self):
        """
        Print all properties of this set with relations
        :return: None
        """
        print("is_reflexive: " + str(self.is_reflexive()))
        print("is_irreflexive: " + str(self.is_irreflexive()))
        print("is_symmetrisch: " + str(self.is_symmetric_relation()))
        print("is_asymmetrisch: " + str(self.is_asymmetric_relation()))
        print("is_antisymmetrisch: " + str(self.is_antisymmetric_relation()))
        print("is_transitiv: " + str(self.is_transitive()))


class RelationMathSetConstDictType(ConstDictType):
    def __init__(self, data, identity=None):
        """
        :type data: dict[str, set[tuple]]
        :type identity: RelationMathSet | None
        :raises ValueError:
        """
        _const = dict()
        for letter in data.keys():
            _const[letter] = RelationMathSet(data[letter], identity, CONST_WAY)
            _const[letter].correct_way()
        super().__init__(_const)


class RelationMathSetResultType(ResultType):
    _result: RelationMathSet

    def __init__(self, data, identity):
        """
        Constructor method
        :type data: set[tuple]
        :type identity: RelationMathSet | None
        """
        super().__init__(RelationMathSet(data, identity, RESULT))


class RelationMathSetIdentityType(ResultType):
    _result: RelationMathSet

    def __init__(self, data):
        """
        Constructor method
        :type data: set[(int, int)]
        """
        super().__init__(RelationMathSet(data, None, IDENTITY_WAY).is_identity(True))
