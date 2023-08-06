#!/usr/bin/env python3
# coding: utf-8

from itertools import combinations_with_replacement, product, chain, compress
from SetSolver1.SimpleMathSet import SimpleMathSet
from SetSolver1.MODE import MODE, CHOOSE_BY_INDEX, RESULT, CONST_WAY
import SetSolver1.MODE
import SetSolver1.helper.update
from SetSolver1.helper.BaseTypes import ConstDictType, ResultType
from SetSolver1.MathSet import MathSet
from SetSolver1.RelationMathSet import RelationMathSet
from SetSolver1.ResultWay import ResultWay


def tools(t, x, y, overflow):
    """
    Switch tool by MODE t
    For tool use variables x and y
    :type t: MODE
    :type x: MathSet
    :type y: MathSet | None
    :type overflow: int
    :rtype: MathSet | None
    :raises ValueError:
    """
    match CHOOSE_BY_INDEX.index(t):
        case 0:
            return x.union(y)
        case 1:
            return x.complement(y)
        case 2:
            return x.intersection(y)
        case 3:
            return x.composition(y)
        case 4:
            if x.total_deep_len() >= (overflow / 2):
                return None
            return x.power_set()
        case 5:
            return x.converse_relation()
        case 6:
            return x.reflexive_closure()
        case 7:
            return x.transitive_closure()
        case 8:
            return x.multi_set_difference(y)
        case 9:
            return x.disjoint_union(y)
        case _:
            raise ValueError("value not found")


def format_way_helper(operand, reversed_const_dict, results):
    """
    Create a string for way by operand
    :type operand: MathSet | None
    :type reversed_const_dict: dict[MathSet, str]
    :type results: set[MathSet]
    :rtype: str
    :raises SyntaxError:
    """
    if operand is None:
        return ""
    elif operand in reversed_const_dict:
        return reversed_const_dict[operand]
    else:
        if operand in results:
            for a in results:
                if operand == a:
                    return format_way(a.way, reversed_const_dict, results)
    raise SyntaxError()


def format_way(way, reversed_const_dict, results):
    """
    make way printable
    :type way: (MODE, (MathSet | None), (MathSet | None))
    :type reversed_const_dict: dict[MathSet, str]
    :type results: set[MathSet]
    :rtype: str
    :raises SyntaxError:
    """
    operator, operand1, operand2 = way
    try:
        way_string = operator.format(format_way_helper(operand1, reversed_const_dict, results),
                                     format_way_helper(operand2, reversed_const_dict, results))
    except SyntaxError:
        raise SyntaxError(way)
    return way_string


def found_result(reversed_const_dict, result, results, do_print):
    """
    search for 'result' in 'results'
    if found return it else None
    :type reversed_const_dict: dict[MathSet, str]
    :type result: MathSet
    :type results: set[MathSet]
    :type do_print: bool
    :rtype: MathSet | None
    """
    for a in results:
        if result.value == a.value:
            if do_print:
                print("Calculated result: " + format_way(a.way, reversed_const_dict, results) + " --> " + str(a))
            return a
    return None


def search(const_dict, result, not_allowed=None, identity=None, overflow=30, range_int=20, do_print=True):
    """
    Search for way to get from consts by 'const_dict' to result
    :type const_dict: dict[str, set[frozenset | int | tuple] | MathSet] | ConstDictType
    :type result: set[frozenset | int | tuple] | MathSet | ResultType
    :type not_allowed: list[MODE]
    :type identity: RelationMathSet | None
    :type overflow: int
    :type range_int: int
    :type do_print: bool
    :rtype: ResultWay | None
    :raises ValueError:
    """
    if not_allowed is None:
        not_allowed = SetSolver1.MODE.DEFAULT_NOT_ALLOWED

    # UPDATE const_dict with frozen-sets to const_dict with MathSets
    for y in const_dict.keys():
        if type(const_dict[y]) == set:
            if sum(1 for x in const_dict[y] if type(x) != tuple) == 0:
                const_dict[y] = RelationMathSet(const_dict[y], identity, CONST_WAY)
            else:
                const_dict[y] = SimpleMathSet(SetSolver1.helper.update.to_tiny_math_set(const_dict[y]), CONST_WAY)
            const_dict[y].correct_way()

    const_dict: dict[str, MathSet] | ConstDictType
    consts = list(const_dict.values())
    if consts == set(consts):
        raise ValueError('the dictionary values of set constants must be unique')
    reversed_const_dict = dict((v, k) for k, v in const_dict.items())
    sorted_results = sorted_consts = sorted(consts, key=lambda i: i.sort_key())

    # UPDATE result with frozen-sets to result with MathSets
    if type(result) == set:
        result = SimpleMathSet(SetSolver1.helper.update.to_tiny_math_set(result), RESULT)
    if isinstance(result, ResultType):
        result = result.get()
    result: MathSet

    very_cool = [1 if x.is_multi_mode() else 0 for x in SetSolver1.MODE.SORTED_CHOOSE_BY_INDEX if x not in not_allowed]

    results: set[MathSet] = set(consts)

    for mode in (1, 2):
        len_results_old = None
        for len_obj in range(range_int):
            len_results = len(results)
            print(str(mode) + ": " + str(round((len_obj/(range_int-1))*100)) + "% / " + str(len_results))\
                if do_print else None
            if len_results == len_results_old:
                break  # performance optimization
            len_results_old = len_results
            if mode == 1:
                my_iter = product(
                        sorted_results,
                        chain(
                            *(
                                product(
                                    sorted_consts if x.is_multi_mode() else [False],
                                    [x]
                                ) for x in SetSolver1.MODE.SORTED_CHOOSE_BY_INDEX if x not in not_allowed)
                        )
                )
                iter_list = list()
                for x, (y, c) in my_iter:
                    iter_list.append((x, y, c))
            else:
                my_iter = compress(
                    product(
                        combinations_with_replacement(sorted_results, 2),
                        [x for x in SetSolver1.MODE.SORTED_CHOOSE_BY_INDEX if x not in not_allowed]
                    ), [
                        1 if x or y == len(sorted_results)-z-1 else 0
                        for z in range(len(sorted_results))
                        for y in range(len(sorted_results)-z)
                        for x in very_cool
                    ]
                )
                iter_list = list()
                for (x, y), c in my_iter:
                    iter_list.append((x, y, c))

            for x, y, c in iter_list:
                new = tools(c, x, y, overflow)
                results.add(new) if new is not None and new.total_deep_len() <= overflow else None
                if c[2] == 0:
                    new = tools(c, y, x, overflow)
                    results.add(new) if new is not None and new.total_deep_len() <= overflow else None
            valid_result = found_result(reversed_const_dict, result, results, do_print)
            if valid_result is not None:
                return ResultWay(valid_result, const_dict, reversed_const_dict, results)
            sorted_results = sorted(results, key=lambda i: i.sort_key())

    print("Nothing found :(") if do_print else None
    return None
