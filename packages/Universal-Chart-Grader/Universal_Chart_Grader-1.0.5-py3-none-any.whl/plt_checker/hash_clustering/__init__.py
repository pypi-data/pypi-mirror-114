from .hashing_clustering import gen_hash_clustering


class Point:
    def __init__(self, x, y, idx, tag):
        self.x = x
        self.y = y
        self.idx = idx
        self.tag = tag

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        else:
            assert item == 1
            return self.y


def avg(points):
    x = sum([x for x, y in points]) / len(points)
    y = sum([y for x, y in points]) / len(points)
    return x, y


def gen_tagged_points(points, tag):
    return [Point(x, y, idx, tag) for idx, (x, y) in enumerate(points)]


def fuse(pos_list):
    groups = gen_hash_clustering(pos_list)
    group_centers = [avg([pos_list[idx] for idx in group]) for group in groups]

    trans = {idx: group_idx
             for group_idx, group in enumerate(groups)
             for idx in group}
    return group_centers, trans


def match_by_clustering(points_computed, points_expected):
    """
    Match the input list of points.
    All points in the expected set must be matched. Some points in the computed set could be leftover.
    """

    COMPUTED = 0
    EXPECTED = 1

    tagged_computed = [Point(x, y, idx, COMPUTED) for idx, (x, y) in enumerate(points_computed)]
    tagged_expected = [Point(x, y, idx, EXPECTED) for idx, (x, y) in enumerate(points_expected)]
    tagged_all = [*tagged_computed, *tagged_expected]

    ok = True
    groups = gen_hash_clustering(tagged_all)
    group_centers = [avg([tagged_all[idx] for idx in group]) for group in groups]
    groups_group_centers = list(sorted(zip(group_centers, groups), key=lambda center_group:center_group[0]))
    group_centers, groups = list(zip(*groups_group_centers))

    for group in groups:
        n_tag1 = len([tagged_all[idx] for idx in group if tagged_all[idx].tag == COMPUTED])
        n_tag2 = len([tagged_all[idx] for idx in group if tagged_all[idx].tag == EXPECTED])
        if n_tag2 != n_tag1:
            ok = False
            break

    trans0 = {tagged_all[idx].idx: group_idx
              for group_idx, group in enumerate(groups)
              for idx in group
              if tagged_all[idx].tag == COMPUTED}

    trans1 = {tagged_all[idx].idx: group_idx
              for group_idx, group in enumerate(groups)
              for idx in group
              if tagged_all[idx].tag == EXPECTED}

    return ok, group_centers, (trans0, trans1)
