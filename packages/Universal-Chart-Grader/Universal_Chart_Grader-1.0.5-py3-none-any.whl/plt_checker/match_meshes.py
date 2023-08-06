import copy
from itertools import groupby

import numpy as np
import pyprnt
from .exceptions import CheckerError, CheckerException

from .hash_clustering import fuse, match_by_clustering


def _to_canonical(vertices):
    """
    Compute the canonical representation of a list of vertices where the list is right rotated until the smallest index become the first element of the input list

    Args
        vertices: List[int]
        orientation: str - either 'clockwise' or 'counterclockwise'
    Returns
        Canonical form of the input list: List[int]
    """

    idx = np.argmin(vertices)

    if not np.isscalar(idx):
        raise CheckerError('duplicate index in indices list')

    return vertices[idx:] + vertices[:idx]


def _match_indices(verts0, verts1, mode):
    """
    match two list of indices of polygon vertices

    Args:
        verts0: List[int]
        verts1: List[int]
        mode: str - either 'orientation' or 'order' or 'set'
            If match mode is orientation, the canonical form of the two lists much be equal
            If match mode is order, the canonical form of verts1 or its reverse equals the canonical form of verts0
            If match mode is set, set(verts0) == set(verts1)

    Returns:
        Boolean
    """

    if len(verts0) != len(verts1):
        return False

    if mode == 'set':
        return set(verts0) == set(verts1)

    verts0 = _to_canonical(verts0)
    verts1 = _to_canonical(verts1)

    if mode == 'orientation':
        return verts0 == verts1
    elif mode == 'order':
        verts1_r = _to_canonical(list(reversed(verts1)))
        return verts0 == verts1 or verts0 == verts1_r
    else:
        raise CheckerError('Unexpected mode ' + mode)


def convert_meshlist(mesh_list):
    """
    Convert a list of meshes to a big mesh with the top level attributes of the mesh pushed down to individual markers in the topology

    Args:
        mesh_list

    Returns:
        A combined Mesh with all top-level attributes moved to markers
    """

    # Compute new positions
    topology = []
    new_positions = []
    for mesh in mesh_list:
        idx_mapping = {}
        for old_idx, pos in enumerate(mesh.positions):
            idx_mapping[old_idx] = len(new_positions)
            new_positions.append(pos)
        for indices, marker in mesh.topology:
            new_indices = tuple([idx_mapping[old_idx] for old_idx in indices])
            new_topo_elem = {}
            new_topo_elem.update({k: v for k, v in mesh.items() if k not in ['positions', 'topology']})
            new_topo_elem.update({key: val for key, val in marker.items()})
            new_topo_elem = tuple(new_topo_elem.items())
            topology.append((new_indices, new_topo_elem))

    return {'positions': new_positions, 'topology': topology}


def reindex(mesh, indices_trans):
    """
    Reindex indices in mesh's topology based on indices_trans
    The old mesh is NOT mutated

    Args:
        mesh
        indices_trans: int -> int

    Returns:
        Reindexed Mesh
    """
    new_mesh = copy.copy(mesh)
    for idx, (indices, markers) in enumerate(new_mesh['topology']):
        new_indices = tuple([indices_trans[index] for index in indices])
        new_mesh['topology'][idx] = new_indices, markers
    return new_mesh


def remove_attrs(mesh, exclude_attrs):
    """ Return a new mesh with attributes removed from both the top level (if any) and the markers """
    new_topology = []
    for indices, marker in mesh.topology:
        new_marker = marker.__class__(**{k: v for k, v in marker.items() if k not in exclude_attrs})
        new_topology.append((indices, new_marker))

    new_mesh = mesh.__class__(**{k: v for k, v in mesh.items() if k not in [*exclude_attrs, 'topology']})
    new_mesh.topology = new_topology
    return new_mesh


def format_kwarg(d):
    s = ''
    for key, val in d.items():
        s += f'{key}={val}, '
    return s[:-2]


def match_meshes(exclude_attrs=('size', 'width', 'color', 'type'), check_indices_mode='set', check_topology=False):
    """
    Match two list of meshes.

    Args
        marker_attrs: List[str] - List of UHE field names to check. Possible names are 'style', 'size', 'color', 'facecolor', 'zorder', 'indices'
        check_indices_mode: str - Either 'orientation' or 'order' or 'set'. See the docstring of match_indices()
        check_topology: boolean - If false, for example, two overlaid vertices will be treated as the same one
w
    Returns
        Callable(mesh_list0, mesh_list1)
    """

    def func(mesh_list0, mesh_list1, test):
        id0, id1 = id(mesh_list0), id(mesh_list1)

        if mesh_list0 == [] and mesh_list1 == []:
            return True

        # remove excluded attrs
        mesh_list0 = [remove_attrs(mesh, exclude_attrs) for mesh in mesh_list0]
        mesh_list1 = [remove_attrs(mesh, exclude_attrs) for mesh in mesh_list1]

        # merge two list of meshes into two unified meshes
        mesh0 = convert_meshlist(mesh_list0)  # TODO Comparable
        mesh1 = convert_meshlist(mesh_list1)

        ### Match vertice positions
        if check_topology is False:
            # fuse duplicate vertex positions in each unified mesh
            mesh0['positions'], trans0 = fuse(mesh0['positions'])
            mesh1['positions'], trans1 = fuse(mesh1['positions'])
            mesh0 = reindex(mesh0, trans0)
            mesh1 = reindex(mesh1, trans1)

        # match the computed and expected positions for the unified meshes
        ok, new_pos, (trans0, trans1) = match_by_clustering(mesh0['positions'], mesh1['positions'])
        if not ok:
            s = 'the computed and the expected ' + test.red_ucs_path_name() + ' mismatch'

            if test.fun_name == 'plot_earth_orbit' and (0, 0) in mesh0['positions']:
                s += "\nHint: Remove the additional sun"
            elif test.fun_name == 'plot_newton' and len(mesh0['positions']) == 0:
                s += "\nHint: Plot the complex numbers in roots as red dots overlaid on the image to identify each basin"

            pyprnt.red_object_ids.add(id0)
            exp = CheckerException(s)
            exp.debug_info = 'geometry mismatch'
            raise exp

        mesh0['positions'] = new_pos
        mesh1['positions'] = new_pos
        mesh0 = reindex(mesh0, trans0)
        mesh1 = reindex(mesh1, trans1)

        ### Match markers
        if len(mesh0['topology']) != len(mesh1['topology']):
            exp = CheckerException('the computed and the expected ' + test.red_ucs_path_name() + ' mismatch')
            exp.debug_info = 'topology mismatch'

            pyprnt.red_object_ids.add(id0)
            raise exp

        # reorder marker indices into canonical form
        for idx in range(len(mesh0['topology'])):
            mesh0['topology'][idx] = _to_canonical(mesh0['topology'][idx][0]), mesh0['topology'][idx][1]
        for idx in range(len(mesh1['topology'])):
            mesh1['topology'][idx] = _to_canonical(mesh1['topology'][idx][0]), mesh1['topology'][idx][1]

        # align the markers by indices
        def key(marker):
            first_key = tuple(sorted(marker[0]))  # sorted indices
            second_key = tuple({k: v for k, v in marker[1] if k not in [*exclude_attrs, 'zorder']}.items())  # indices
            return first_key, second_key  # TODO other attributes

        mesh0['topology'] = list(sorted(mesh0['topology'], key=key))
        mesh1['topology'] = list(sorted(mesh1['topology'], key=key))

        # match indices
        for idx in range(len(mesh0['topology'])):
            indices0, _ = mesh0['topology'][idx]
            indices1, _ = mesh1['topology'][idx]
            if not _match_indices(indices0, indices1, mode=check_indices_mode):
                pyprnt.red_object_ids.add(id0)
                exp = CheckerException('the computed and the expected ' + test.red_ucs_path_name() + ' mismatch')
                exp.debug_info = 'topology mismatch'
                raise exp

        # match zorder
        def get_key(tup, key):
            for k, v in tup:
                if k == key:
                    return v

            assert False

        key_zorder = lambda indice_marker: get_key(indice_marker[1], 'zorder')
        second_elem = lambda zorder0_zorder1: zorder0_zorder1[1]
        zorders0_zorders1 = [(key_zorder(mesh0['topology'][idx]),
                              key_zorder(mesh1['topology'][idx])) for idx in range(len(mesh0['topology']))]
        groups = [list(g) for k, g in groupby(sorted(zorders0_zorders1, key=second_elem), key=second_elem)]

        for idx in range(len(groups) - 1):
            this_group = groups[idx]
            next_group = groups[idx + 1]

            max_zorder1_this, _ = max(this_group, key=lambda zorder0_zorder1: zorder0_zorder1[0])
            min_zorder1_next, _ = min(next_group, key=lambda zorder0_zorder1: zorder0_zorder1[0])
            if not (max_zorder1_this < min_zorder1_next):
                pyprnt.red_object_ids.add(id0)
                exp = CheckerException('zorder mismatch for the computed and expected ' + test.red_ucs_path_name())
                exp.debug_info = 'zorder mismatch'
                raise exp


        # match marker
        indice_marker_list0 = mesh0['topology']
        indice_marker_list1 = mesh1['topology']
        for idx in range(len(mesh0['topology'])):
            _, marker0 = indice_marker_list0[idx]
            _, marker1 = indice_marker_list1[idx]
            for key, val in marker1:
                if key == 'zorder': continue

                if get_key(marker0, key) != get_key(marker1, key):
                    # print(marker0)
                    # print(marker1)
                    # print(key)

                    s = 'the computed and expected ' + test.red_ucs_path_name() + ' mismatch'

                    if test.fun_name == 'plot_earth_coords':
                        flag = False
                        for indices, marker in mesh0['topology']:
                            if flag is False:
                                for key, val in marker:
                                    if key == 'axes' and 2 in val:
                                        flag = True
                                        break
                        if flag:
                            s += '\nHint: Use two line plot instead of twin axis'

                    pyprnt.red_object_ids.add(id0)
                    exp = CheckerException(s)
                    exp.debug_info = 'topology mismatch'
                    raise exp

    # env = locals()
    # env.pop('func')
    # func.__dict__.update(env)
    return func
