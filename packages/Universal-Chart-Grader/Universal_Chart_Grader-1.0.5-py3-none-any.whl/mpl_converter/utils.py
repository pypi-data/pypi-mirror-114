import sys
from collections import namedtuple
from datetime import datetime
import operator

import matplotlib.dates as mdates, matplotlib.colors as mcolors
import scipy.interpolate
import numpy as np
from numpy import pi


def rad_2pi(rad):
    """
    Args:
        rad: Angle in range [-pi, pi]

    Returns:
        Angle in range [0, 2*pi]
    """
    if rad < 0:
        return 2 * pi + rad
    return rad


def cast_float(na):
    """

    Args:
        na: `datetime.datetime` or `numpy.datetime64` or List of these

    Returns:
        float value or np.ndarray whose dtype=float
    """

    if isinstance(na, np.ndarray):
        na = na.tolist()

    if isinstance(na, (datetime, np.datetime64)):
        return mdates.date2num(na)
    elif isinstance(na, list) and isinstance(na[0], (datetime, str)):
        if isinstance(na[0], str):
            return np.array([mdates.date2num(datetime.strptime(elem, '%Y-%m-%d')) for elem in na])
        return np.array([mdates.date2num(elem) for elem in na])
    else:
        return np.array([float(elem) for elem in na])


ROUND_DIGIT = 2


def round_float(na):
    return np.round_(na, ROUND_DIGIT)


def make_dict(filter, d=None, **kwargs):
    """
    Make a filtered dictionary

    Args
        filter: Object->bool, whether to include an key:val pair or not
        d: dictionary
    Returns
        dict
    """

    if dict is None:
        d = kwargs
    d = {key: val for key, val in d.items() if not filter(key, val)}
    return d


np.set_printoptions(precision=2, threshold=4)


def add_knots(cmap, knot_list):
    """ add knots to an UHE colormap """

    cmap_func = uhe_to_func(cmap)
    new_cmap = cmap.copy()
    knot_list = sorted([knot for knot in knot_list if knot not in cmap[:, 0]])
    if len(knot_list) == 0:
        return new_cmap
    color_list = np.array([cmap_func(new_knot) for new_knot in knot_list])
    knot_list = np.array(knot_list).reshape(-1, 1)
    new_rows = np.concatenate((knot_list, color_list), axis=1)

    idx1, idx2 = 0, 0
    while idx2 < len(new_rows):
        while idx1 < len(new_cmap) and new_cmap[idx1, 0] < new_rows[idx2, 0]:
            idx1 += 1
        new_cmap = np.insert(new_cmap, idx1, new_rows[idx2], axis=0)
        idx1 += 1
        idx2 += 1
    return new_cmap


def uhe_to_func(cmap):
    """
    Convert a Colormap in Universal hierarchy representation to python Callable

    Args:
        cmap: UHE colormap (refer to the top of this file)

    Returns:
        python Callable
    """

    vals, colors = cmap[:, 0], cmap[:, 1:]
    return lambda x: scipy.interpolate.interp1d(vals, np.array(colors).T)(x).T


def dist(cmap1, cmap2, op=operator.sub):
    diff_result = diff(cmap1, cmap2, op)
    return abs(diff_result[:, 1:]).m()


def diff(cmap1, cmap2, op=operator.sub):
    """ compute the difference of two colormaps with knots interpolated """

    knot1 = cmap1[:, 0]
    knot2 = cmap2[:, 0]
    new_cmap1 = add_knots(cmap2, knot1)
    new_cmap2 = add_knots(cmap1, knot2)
    knot_diff = []
    cmap_diff = []

    i1, i2 = 0, 0
    assert new_cmap1[0, 0] == new_cmap2[0, 0]
    while i1 < len(new_cmap1):
        assert i2 < len(new_cmap2)
        j1, j2 = i1, i2
        while j1 < len(new_cmap1) and new_cmap1[i1, 0] == new_cmap1[j1, 0]:
            j1 += 1
        while j2 < len(new_cmap2) and new_cmap2[i2, 0] == new_cmap2[j2, 0]:
            j2 += 1

        assert i1 + 1 <= j1 <= i1 + 2
        assert i2 + 1 <= j2 <= i2 + 2
        if j1 == i1 + 2 and j2 == i2 + 2:
            knot_diff.append(new_cmap1[i1, 0])
            knot_diff.append(new_cmap1[i1, 0])
            cmap_diff.append(op(new_cmap1[i1, 1:], new_cmap2[i2, 1:]))
            cmap_diff.append(op(new_cmap1[i1 + 1, 1:], new_cmap2[i2 + 1, 1:]))
        elif j1 == i1 + 2:
            knot_diff.append(new_cmap1[i1, 0])
            knot_diff.append(new_cmap1[i1, 0])
            cmap_diff.append(op(new_cmap1[i1, 1:], new_cmap2[i2, 1:]))
            cmap_diff.append(op(new_cmap1[i1 + 1, 1:], new_cmap2[i2, 1:]))
        elif j2 == i2 + 2:
            knot_diff.append(new_cmap1[i1, 0])
            knot_diff.append(new_cmap1[i1, 0])
            cmap_diff.append(op(new_cmap1[i1, 1:], new_cmap2[i2, 1:]))
            cmap_diff.append(op(new_cmap1[i1, 1:], new_cmap2[i2 + 1, 1:]))
        else:
            knot_diff.append(new_cmap1[i1, 0])
            cmap_diff.append(op(new_cmap1[i1, 1:], new_cmap2[i2, 1:]))
        i1, i2 = j1, j2

    return np.concatenate((np.array(knot_diff).reshape(-1, 1), np.array(cmap_diff)), axis=1)


def diff_hsv(cmap1, cmap2):
    """ compute the difference of two colormaps with knots interpolated """

    def op(color1, color2):
        hsv1 = mcolors.rgb_to_hsv(color1 / 255)
        hsv2 = mcolors.rgb_to_hsv(color2 / 255)
        return hsv1 - hsv2

    return diff(cmap1, cmap2, op)


EPSILON = 0  # offset of jump point
CMAPEQ_THRESHOLD = 25  # error threshold for the colormaps defined as "same"