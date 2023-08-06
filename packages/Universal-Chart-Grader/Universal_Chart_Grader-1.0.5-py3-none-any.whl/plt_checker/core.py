"""
Unified testing code for all projects in Data Visualization
"""

import io, re, copy
import traceback
from collections import Mapping
from enum import Enum

import dill as pickle

import mpl_converter
from plt_checker.atomic_methods import *
from .exceptions import *


class PlotTests:
    """
    Class for creating, saving, loading, and checking tests for projects
    """

    def __init__(self, fun_names, record_tests=False):
        """
        Input: List fun_names of string, optional dict {fun_name:UCS}, optional Boolean record_tests,

        Output: ProjectTests object containing dictionary of test cases
        keyed by fun_name
        """

        self.test_cases = {}

        for name in fun_names:
            self.test_cases[name] = []

        self.record_tests = record_tests
        self.pause_add_test = 0

    def add_test(self, fun_name, test_case):
        """
        Input: string fun_name, input/output pair test_case

        Action: Append test_case to corresponding entry in test case dictionary
        """

        if self.record_tests and self.pause_add_test == 0:
            self.test_cases[fun_name].append(copy.copy(test_case))

    def pause_tests(self):
        """
        Action: Pausing recording of tests via add_test()

        Note that multiple pause_tests() stack
        """

        self.pause_add_test += 1

    def resume_tests(self):
        """
        Action: Resume recording of tests via add_test()

        Note that multiple resume_tests() clear stacked pause_tests()
        """

        self.pause_add_test -= 1

    def save_tests(self, project_name):
        """
        Input: string project_name

        Action: Save test cases for project in pickle file
        """

        if self.record_tests:
            for fun_name in self.test_cases:
                print("Generated", len(self.test_cases[fun_name]), "test cases for", fun_name + "()")

            with open(project_name, 'wb') as file:
                pickle.dump(self, file)

    def check_tests(self, student, checker_dict, path_dict, caller_env):
        checker = PlotTestChecker(self.test_cases, path_dict, caller_env)
        checker.check_tests(student, checker_dict)


class PlotTestChecker:
    show_path = 0
    print_error = 0

    def __init__(self, test_cases, path_dict, caller_env):
        self.test_cases = test_cases
        self.result_dict = {}

        ## Injected fields
        # checker_dict
        self.path_dict = path_dict
        self.caller_env = caller_env
        self.checker_dict = None
        self.student = None
        # function
        self.fun_name = None
        self.fun_pts = None
        # case
        self.case_idx = None
        # UCM & path
        self.computed_ucm = None
        self.expected_ucm = None
        self.chart_spec = None
        self.ucs_path = None
        self.compUCM_path = None

    def check_tests(self, student, checker_dict):
        self.student = student
        self.checker_dict = checker_dict

        for fun_name, (chart_spec, fun_pts) in checker_dict.items():
            try:
                self._check_test(fun_name, chart_spec, fun_pts)
                self.result_dict[self.fun_name] = True
                print(self.passed())
            except CheckerException as exp:
                self.result_dict[self.fun_name] = exp
                s = self.failed() + ', '
                if PlotTestChecker.show_path:
                    s += 'on the UCM path ' + Color(self.ucs_path, fg='red') + '. '
                s += str(exp) + '.'
                print(s)
                # traceback.print_exc()
            except BaseException as exp:
                self.result_dict[self.fun_name] = exp
                if PlotTestChecker.print_error:
                    traceback.print_exc()
                else:
                    print(self.passed())

    def _check_test(self, fun_name, chart_spec, fun_pts):
        self.fun_name, self.chart_spec, self.fun_pts = fun_name, chart_spec, fun_pts

        for self.case_idx, (inputs, self.expected_ucm) in enumerate(self.test_cases[self.fun_name]):
            # Run student's plotting method
            try:
                fun_def = getattr(self.student, self.fun_name)
                computed_fig = fun_def(*inputs)
            except Exception as err:
                traceback.print_exc()
                raise StudentError()

            if computed_fig is None:
                raise CheckerException("the plotting method doesn't return the figure object")

            # Save student's plot to a buffer
            self.img = mpl_converter.save_img(computed_fig)

            # Convert student's figure to UCM
            try:
                self.computed_ucm = mpl_converter.mpl_convert(computed_fig)
            except Exception:
                raise UCMConversionFailure()

            mpl_converter.cleanup(computed_fig)

            # Enable students to view the UCM and the image in checker notebook
            if isinstance(inputs, dict):
                self.caller_env[self.fun_name + '_input'] = inputs
            else:
                self.caller_env[self.fun_name + '_input'] = {fun_def.__code__.co_varnames[i]: inputs[i] for i in range(len(inputs))}

            self.caller_env[self.fun_name + '_output'] = self.img
            self.caller_env[self.fun_name + '_studentUCM'] = self.computed_ucm
            self.caller_env[self.fun_name + '_instructorUCM'] = self.expected_ucm

            # Check UCS item by item
            self.match_ucs(self.computed_ucm, self.expected_ucm, self.fun_name, self.chart_spec, self.fun_name)

    def match_ucs(self, sub_computed_ucm, sub_expected_ucm, compUCM_path, chart_spec, ucs_path):
        """ Match computed UCM against expected UCM and UCS recursively """
        self.ucs_path = ucs_path
        self.compUCM_path = compUCM_path

        # print(self.ucs_path)

        # Handle leaves of UCS
        if not isinstance(chart_spec, (list, dict)):
            if not callable(chart_spec):
                chart_spec = constant_to_callable(chart_spec)
            chart_spec(sub_computed_ucm, sub_expected_ucm, self)
            return

        # Non-leaves of UCS
        def get_iter(list_or_dict):
            if isinstance(list_or_dict, list):
                return range(len(list_or_dict))
            elif isinstance(list_or_dict, Mapping):
                return list_or_dict.keys()
            else:
                raise CheckerError('Unexpected type: ' + repr(list_or_dict))

        ucs_keys = list(get_iter(chart_spec))
        ucm_keys = list(get_iter(sub_computed_ucm))

        # Sanity check: All ucs_keys should be matched with at least 1 ucm_key
        def match_keys(ucm_keys, ucs_keys):
            """ Sanity check: All ucs_keys should be matched with at least 1 ucm_key """

            for ucs_key in ucs_keys:
                matched_keys = [k for k in ucm_keys if re.match('^' + str(ucs_key) + '$', str(k)) is not None]
                if len(matched_keys) == 0:
                    self.ucs_path += f'.{ucs_key}' if isinstance(sub_computed_ucm,
                                                                 Mapping) else f'[{ucs_key}]'  # isinstance(computed_ucm, list)
                    raise CheckerException(self.red_ucs_path_name() + ' is missing')

        match_keys(ucm_keys, ucs_keys)

        for ucs_key in ucs_keys:
            matched_keys = [k for k in ucm_keys if re.match('^' + str(ucs_key) + '$', str(k)) is not None]
            for ucm_key in matched_keys:
                if isinstance(chart_spec, dict):
                    next_ucs_path = f'{ucs_path}.{ucs_key}'
                else:
                    next_ucs_path = f'{ucs_path}[{ucs_key}]'

                if isinstance(sub_computed_ucm, Mapping):
                    next_compUCM_path = f'{compUCM_path}.{ucm_key}'
                else:
                    next_compUCM_path = f'{compUCM_path}[{ucm_key}]'

                self.match_ucs(sub_computed_ucm[ucm_key], sub_expected_ucm[ucm_key], next_compUCM_path,
                               chart_spec[ucs_key], next_ucs_path)

    def failed(self, partial=0):
        """ Failed inside a test case """

        return f'{self.fun_name}() FAILED on test case {self.case_idx}'

    def passed(self):
        """ Pass all test cases for a method """

        s = f'{self.fun_name}() PASSED all tests.'
        return s

    def red_ucs_path_name(self, color='red'):
        path_mapped = self.path_dict[self.ucs_path] if self.ucs_path in self.path_dict else self.ucs_path
        return Color(path_mapped, fg=color)

    def red_path(self, color='red'):
        return Color(self.compUCM_path, fg=color)

    def dump(self):
        s = io.StringIO()
        print(f'fun_name={self.fun_name} fun_pts={self.fun_pts}', file=s)
        print(f'case_idx={self.case_idx}', file=s)
        print(f'ucs_path={self.ucs_path}', file=s)
        print(f'compUCM_path={self.compUCM_path}', file=s)
        print(f'computed_ucm', file=s)
        pyprnt.prnt(self.computed_ucm, file=s)
        print(f'expected_ucm', file=s)
        pyprnt.prnt(self.expected_ucm, file=s)
        print('chart_spec', file=s)
        pyprnt.prnt(self.chart_spec, file=s)
        return s.getvalue()
