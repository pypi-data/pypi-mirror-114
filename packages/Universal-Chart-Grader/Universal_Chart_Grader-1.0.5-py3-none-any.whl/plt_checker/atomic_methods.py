"""
Atomic checker methods for UCS
"""
from numbers import Number

import numpy as np
import pyprnt

from colorstring import Color
# noinspection PyUnresolvedReferences
from .match_meshes import match_meshes
from .exceptions import CheckerException


class OR:
    """Intended to be used with contains_keyword. Please refer to its docstring."""

    def __init__(self, *arr):
        self.arr = [elem for elem in arr]

    def __repr__(self):
        return f"OR({', '.join([repr(elem) for elem in self.arr])})"

    def __str__(self):
        return f"({', '.join([repr(elem) for elem in self.arr])})"

    def __iter__(self):
        return iter(self.arr)


def contains_keyword(*keywords):
    """
    Check keyword in the string.

    Examples
        contains_keyword('kw1', 'kw2', 'kw3') - Checks keyword 'kw1' and 'kw2' and 'kw3'
        contains_keyword('kw1', OR('kw2-variant1', 'kw2-variant2') - checks keyword 'kw1' and one of 'kw2-variant1' and 'kw2-variant2'
    """

    def checker_method(computed, dummy_expected, test):
        computed_id = id(computed)
        computed = computed.lower()

        for text in [txt for txt in keywords if isinstance(txt, str)]:
            if text.lower() not in computed:
                pyprnt.red_object_ids.add(computed_id)
                raise CheckerException(f"{test.red_ucs_path_name()} does not have keyword {repr(text)}")

        for tup in [tup for tup in keywords if isinstance(tup, (tuple, list, OR))]:
            if all(text.lower() not in computed for text in tup):
                pyprnt.red_object_ids.add(computed_id)
                raise CheckerException(f"{test.red_ucs_path_name()} does not have any of the keywords {tup}")

    env = locals()
    env.pop('checker_method')
    checker_method.__dict__.update(env)  # keywords

    return checker_method


def match_array(rtol=0):
    """ Match student's array with the instructor's array """

    def checker_method(computed, expected, test):
        computed_id = id(computed)

        if not isinstance(computed, type(expected)):
            pyprnt.red_object_ids.add(computed_id)
            raise CheckerException(f'The values of computed and expected {test.red_ucs_path_name()} mismatch')

        if isinstance(expected, np.ndarray):
            if not np.allclose(computed, expected, rtol=rtol):
                pyprnt.red_object_ids.add(computed_id)
                raise CheckerException(f'The values of computed and expected {test.red_ucs_path_name()} mismatch')
            return

        if isinstance(expected, list):
            if len(computed) != len(expected):
                pyprnt.red_object_ids.add(computed_id)
                raise CheckerException(f'The length of computed and expected {test.red_ucs_path_name()} mismatch')

        if not np.allclose(computed, expected, rtol=rtol):
            pyprnt.red_object_ids.add(computed_id)
            raise CheckerException(f'The values of computed and expected {test.red_ucs_path_name()} mismatch')

    return checker_method


def match_object():
    """ Match student's object with the instructor's object using object.__eq__() """

    def checker_method(computed, expected, test):
        match_constant = constant_to_callable(expected)
        match_constant(computed, expected, test)

    return checker_method


def match_aspect_ratio():
    """ match the aspect ratio of the computed against the expected """

    def func(computed_range, expected_range, test):
        computed_range_id = id(computed_range)

        computed_ratio = computed_range[1] / computed_range[0]
        expected_ratio = expected_range[1] / expected_range[0]
        if not np.isclose(computed_ratio, expected_ratio):
            pyprnt.red_object_ids.add(computed_range_id)
            raise CheckerException(f'computed and expected {Color("aspect ratio", fg="red")} mismatch')

    return func


def is_evenly_spaced():
    """ Check where the difference between adjacent elements in the array is a constant """

    def func(computed_array, dummy_expected_array, test):
        computed_array_id = id(computed_array)

        if isinstance(computed_array, list):
            if not all(isinstance(elem, Number) for elem in computed_array):
                pyprnt.red_object_ids.add(computed_array_id)
                raise CheckerException(f'Unexpected type encountered in {test.red_ucs_path_name()}')

            computed_array = np.array(computed_array)
        elif not isinstance(computed_array, np.ndarray):
            pyprnt.red_object_ids.add(computed_array_id)
            raise CheckerException(f'Unexpected type encountered in {test.red_ucs_path_name()}')

        deriv = (computed_array[:-1] - computed_array[1:])
        second_deriv = deriv[:-1] - deriv[1:]
        if not np.isclose(np.linalg.norm(second_deriv), 0):
            pyprnt.red_object_ids.add(computed_array_id)
            raise CheckerException(f'{test.red_ucs_path_name()} are not evenly spaced')

    return func


def constant_to_callable(c):
    """ Convert constant leaves of UCS to checker methods """

    def cmp(computed, dummy_expected, test):
        computed_id = id(computed)

        if not isinstance(computed, type(c)):
            pyprnt.red_object_ids.add(computed_id)
            raise CheckerException(f'The values of computed and expected {test.red_ucs_path_name()} mismatch')

        if isinstance(c, np.ndarray):
            if not np.array_equal(computed, c):
                pyprnt.red_object_ids.add(computed_id)
                raise CheckerException(f'The values of computed and expected {test.red_ucs_path_name()} mismatch')
            return

        if isinstance(c, list):
            if len(computed) != len(c):
                pyprnt.red_object_ids.add(computed_id)
                raise CheckerException(f'The length of computed and expected {test.red_ucs_path_name()} mismatch')

        if not (computed == c):
            pyprnt.red_object_ids.add(computed_id)
            raise CheckerException(f'The values of computed and expected {test.red_ucs_path_name()} mismatch')

    return cmp


def exist():
    return lambda computed, expected, test: True
