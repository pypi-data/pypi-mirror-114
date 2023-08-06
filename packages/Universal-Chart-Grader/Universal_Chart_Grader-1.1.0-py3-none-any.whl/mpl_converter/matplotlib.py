"""
This module must be import before the matplotlib module
"""

import functools
import warnings
from numbers import Number

import matplotlib
import matplotlib._cm_listed
import matplotlib.axis as maxis
import matplotlib.cm
import matplotlib.collections as mcollections
import matplotlib.colors as mcolors
import matplotlib.markers
import matplotlib.patches
import matplotlib.projections.polar as mpolar
import matplotlib.pyplot as plt
import matplotlib.text
import mpl_toolkits.mplot3d.axis3d as maxis3d
import numpy as np
import scipy.interpolate
from matplotlib import rcParams
from matplotlib.lines import _get_dash_pattern
# noinspection PyUnresolvedReferences
from mpl_toolkits.mplot3d import Axes3D

from ucm import AngularAxis, Annotation, Colorbar, Coord_Sys, DiscPoint, Figure, Image2D, Legend, Line2D, NamedColor, \
    Network, \
    NonUniformColormap, Polygon, \
    PolyMesh, \
    RadialAxis, RGB255Color, \
    Scatter, \
    Segment, Subplot, Text, UniformColormap, XAxis, YAxis, ZAxis
from . import utils
from .utils import EPSILON, rad_2pi, round_float

null_objs = [[], None, dict(), tuple(), '', dict(text='')]


def mpl_convert(fig):
    return convert_figure(fig)


def totuple(arr):
    if isinstance(arr, Number):
        return arr
    else:
        assert isinstance(arr, (list, type(np.array([]))))
        return tuple([totuple(elem) for elem in arr])


def is_null(key, val):
    if isinstance(val, np.ndarray):
        return len(val.flatten()) == 0
    elif isinstance(val, list):
        return all(is_null('', elem) for elem in val)

    return val in null_objs


make_dict = functools.partial(utils.make_dict, is_null)


def convert_figure(fig):
    fig.canvas.draw()  # force render the figure to make available some fields

    axstack = [ax for (_, ax_info), (_, ax) in fig._axstack if
               '_is_colorbar' not in ax.__dict__]  # _is_colorbar is monkey-patched. See the top of this module.

    # TODO kill this code
    if axstack == []:
        fig = plt.gcf()
        axstack = [ax for (_, ax_info), (_, ax) in fig._axstack if
                   '_is_colorbar' not in ax.__dict__]

    main_axes_list = []  # subplots that are not created by twinx() or twiny()
    while axstack:
        ax0 = axstack[0]
        for sibling in ax0._twinned_axes.get_siblings(ax0):
            if sibling in axstack:  # (is_plt_axes(twinned_axes) == False)
                axstack.remove(sibling)
        main_axes_list.append(ax0)

    return Figure(legends=[convert_legend(legend) for legend in fig.legends],
                  subplots=[convert_subplot(ax) for ax in main_axes_list],
                  title=convert_text(fig._suptitle) if fig._suptitle else None,
                  size=(int(fig.get_size_inches()[0] * fig.get_dpi()), int(fig.get_size_inches()[1] * fig.get_dpi())))


def convert_patch(patch):
    if isinstance(patch, matplotlib.patches.Polygon):
        vertices = patch.xy[:-1]

    else:
        x0, x1, y0, y1 = patch._x0, patch._x1, patch._y0, patch._y1
        vertices = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

    points = []
    indices = []
    for x, y in vertices:
        if (x, y) not in points:
            points.append((x, y))
            index = len(points) - 1
        else:
            index = points.index((x, y))
        indices.append(index)

    polygon = Polygon(edge_color=convert_color(patch.get_edgecolor()),
                      edge_width=patch.get_linewidth(),
                      face_color=convert_color(patch.get_facecolor()) if patch.fill else None,
                      opacity=1 if patch.fill else 0)

    topology = [(tuple(indices), polygon)]
    return PolyMesh(positions=tuple(points), topology=topology, zorder=patch.zorder)


def convert_collection(collection):
    points = []
    point_to_idx = {}
    markers = []

    # '__is_contour_path' field is created in mpl_converter.monkey_patch for collections created by ax.contourf()
    if isinstance(collection, mcollections.PathCollection) and hasattr(collection, '__is_contour_path'):
        verts = collection._paths[0].vertices
        indices = tuple(range(len(verts)))
        r, g, b = collection.get_facecolor()[0][:3]
        color = RGB255Color(r, g, b)
        tuples = [(indices, Polygon(face_color=color))]

        return PolyMesh(positions=verts, topology=tuples, zorder=collection.zorder)

    elif isinstance(collection, mcollections.PathCollection):
        # PathCollection
        # - offsets [(x1, y1), (x2, y2), ...]

        for idx, p in enumerate(collection.get_offsets()):
            p = totuple(p)
            if 'PolarAxesSubplot' in type(collection.axes).__name__:
                r, theta = p
                p = (rad_2pi(theta), r)

            # points
            if p not in points:
                points.append(p)

            # markers
            # ! color of point is calculate by cycling the array of collection.get_facecolor()
            facecolors = collection.get_facecolor() if len(collection.get_facecolor()) != 0 else \
                rcParams['axes.prop_cycle'].by_key()['color']
            color = convert_color(facecolors[idx % len(facecolors)])

            marker_type = match_marker(collection.get_paths()[idx % len(collection.get_paths())])

            marker = marker_type(color=color,
                                 size=collection.get_sizes()[idx % len(collection.get_sizes())])
            markers.append((tuple([len(points) - 1]), marker))

        return Scatter(positions=np.array(points), topology=markers, zorder=collection.zorder)

    elif isinstance(collection, mcollections.LineCollection):
        # LineCollection
        # - segments: List
        #    - segment [[x1,y1], [x2,y2], ...]    (numpy array)
        t = Network

        for idx, seg in enumerate(collection.get_segments()):
            if len(seg) > 2:
                t = PolyMesh

            seg = totuple(seg)

            # points
            indices = []
            for x, y in seg:
                try:
                    index = point_to_idx[(x, y)]
                except KeyError:
                    points.append((x, y))
                    index = len(points) - 1
                    point_to_idx[(x, y)] = len(points) - 1
                indices.append(index)

            # markers
            seg = Segment(color=convert_color(collection.get_color()[idx % len(collection.get_color())]),
                          width=collection.get_linewidth()[idx % len(collection.get_linewidth())],
                          style=convert_linestyle(collection._us_linestyles[idx % len(collection._us_linestyles)]) if
                          collection._us_linestyles[idx % len(collection._us_linestyles)][0] is not None else None)

            markers.append((tuple(indices), seg))

        return t(positions=np.array(points), topology=markers, zorder=collection.zorder)

    else:
        raise TypeError('Unexpected collection type: ' + type(collection))


def convert_image(img):
    return Image2D(vals=np.array(img._A) if img.origin == 'upper' else np.flip(np.array(img._A), axis=0),
                   extents=tuple(img.get_extent()),
                   colormap=cmap_to_uhe(img.get_cmap()),
                   value_range=(img.norm.vmin, img.norm.vmax))


def convert_line(line):
    """
    Convert Matplotlib Line2D object to UHE Mesh
    Args:
        line: matplotlib.lines.Line2D

    Returns:
        UHE Grid
    """

    xs = np.array([float(x) if isinstance(x, Number) else idx for idx, x in enumerate(line.get_xdata())])
    ys = np.array([float(y) if isinstance(y, Number) else idx for idx, y in enumerate(line.get_ydata())])

    if 'PolarAxesSubplot' in type(line.axes).__name__:
        xs, ys = ys, xs
        ys = np.array([rad_2pi(y) for y in ys])

    points = np.concatenate([xs.reshape(-1, 1), ys.reshape(-1, 1)], axis=1)
    colors = line.get_color() if isinstance(line.get_color(), list) else [line.get_color()]
    if len(colors) == 1:
        colors *= len(points)

    seg = Segment(color=convert_color(line.get_color()),
                  width=line._linewidth)
    # 'initial offset' : line._dashOffset,
    # 'on_off_sequence': line._dashSeq,

    topology = [((i, i + 1), seg) for i in range(len(points) - 1)]

    if line.get_marker() == 'o':
        disc = DiscPoint(color=line.get_markerfacecolor(), size=line.get_markersize() ** 2)
        topology += [((i,), disc) for i in range(len(points))]
        if len(points) == 1:
            return Scatter(positions=points, topology=topology, zorder=line.zorder)
        else:
            return Network(positions=points, topology=topology, zorder=line.zorder)
    else:
        return Line2D(positions=points, topology=topology, zorder=line.zorder)


def convert_annotations(anntn):
    return convert_text(anntn, include_position=True)


def convert_subplot(ax):
    """
    Create UHE subplot from Matplotlib Axes which are dynamically generated and therefore matched by name
    """

    (x0, y0), (x1, y1) = ax.figure.transFigure.transform(ax.get_position())
    display_range = x1 - x0, y1 - y0
    # data_aspect_ratio = ax.get_aspect() if ax.get_aspect() != 'equal' else 1
    axis_list = []
    annotations = []
    legends = []
    colorbars = []
    grids = []
    meshes = []

    def get_xaxis(ax):
        if ax.axison and ax.xaxis.get_visible():
            return ax.xaxis

        for axx in ax.get_shared_x_axes().get_siblings(ax):
            if axx is ax: continue
            if axx.axison and axx.xaxis.get_visible():
                return axx.xaxis

    def get_yaxis(ax):
        if ax.axison and ax.yaxis.get_visible():
            return ax.yaxis

        for axx in ax.get_shared_x_axes().get_siblings(ax):
            if axx is ax: continue
            if axx.axison and axx.yaxis.get_visible():
                return axx.yaxis

    if type(ax).__name__ in ['AxesSubplot', 'Axes']:
        # Cartesian 2D Twin axes figure are implemented as overlaid subplots in Matplotlib
        # Therefore, we shall first extract all the subplots of the input subplot, convert each, then merge the result.

        coord_system = Coord_Sys.CARTESIAN_2D
        axis_objs = []
        axes_list = ax._twinned_axes.get_siblings(ax)
        for axes in axes_list:
            axis_objs += [axis for axis in [axes.xaxis, axes.yaxis] if axes.axison and axis.get_visible()]
            legends += [convert_legend(legend) for legend in [axes.legend_] if legend is not None]
            if hasattr(axes, '__colorbar'):
                # '__colorbar' field is added by monkey-patching. See mpl_converter.monkey_patch
                colorbars += [convert_colorbar(cb) for cb in axes.__colorbar]

            attached_axis_list = []
            xaxis = get_xaxis(axes)
            yaxis = get_yaxis(axes)
            if xaxis is not None:
                attached_axis_list.append(axis_objs.index(xaxis))
            if yaxis is not None:
                attached_axis_list.append(axis_objs.index(yaxis))
            attached_axis_list = tuple(attached_axis_list)

            for line in axes.texts:
                converted = convert_annotations(line)
                converted.axes = attached_axis_list
                annotations.append(converted)

            for im in axes.images:
                converted = convert_image(im)
                converted.axes = attached_axis_list
                grids.append(converted)

            for line in axes.lines:
                converted = convert_line(line)
                converted.axes = attached_axis_list
                meshes.append(converted)

            for collection in axes.collections:
                converted = convert_collection(collection)
                converted.axes = attached_axis_list
                meshes.append(converted)

            for patch in axes.patches:
                converted = convert_patch(patch)
                converted.axes = attached_axis_list
                meshes.append(converted)

            meshes.sort()

        axis_list += list(sorted([convert_axis(axis) for axis in axis_objs]))
    else:
        # if type(ax).__name__ == 'Axes3DSubplot':
        #     coord_system = Coord_Sys.CARTESIAN3D
        #     axis_list += [convert_axis(axis) for axis in [ax.xaxis, ax.yaxis, ax.zaxis] if ax.axison]
        #
        # elif type(ax).__name__ == 'PolarAxesSubplot':
        #     coord_system = Coord_Sys.POLAR2D
        #     axis_list += [convert_axis(axis) for axis in [ax.xaxis, ax.yaxis] if ax.axison]
        # else:
        raise RuntimeError('Unexpected Matplotlib subplot type')

        # legends += [convert_legend(legend) for legend in [ax.legend_] if legend is not None]
        # colorbars += [convert_colorbar(im.colorbar) for im in ax.images if im.colorbar is not None]
        # annotations += [{**convert_annotations(anntn), 'axes': axis_list} for anntn in ax.texts]
        # grids += [{**convert_image(im), 'axes': axis_list} for im in ax.images]
        # meshes += [{**convert_line(line), 'axes': axis_list} for line in ax.lines]
        # meshes += [{**convert_collection(collection), 'axes': axis_list} for collection in ax.collections]
        # meshes += [{**convert_patch(patch), 'axes': axis_list} for patch in ax.patches]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        rowNum = ax.rowNum if hasattr(ax, 'rowNum') else None
        colNum = ax.colNum if hasattr(ax, 'colNum') else None

    return Subplot(pos=(rowNum, colNum),
                   title=convert_text(ax.title, include_position=False) if ax.get_title() != '' else None,
                   coordinates_system=coord_system,
                   display_range=display_range,
                   axes=axis_list,
                   legends=legends,
                   colorbars=colorbars,
                   annotations=annotations,
                   grids=grids,
                   meshes=meshes)


def convert_axis(axis):
    subplot_cls_name_mapping = {
        maxis.XAxis      : XAxis,
        maxis3d.XAxis    : YAxis,
        maxis.YAxis      : YAxis,
        maxis3d.YAxis    : YAxis,
        maxis3d.ZAxis    : ZAxis,
        mpolar.ThetaAxis : AngularAxis,
        mpolar.RadialAxis: RadialAxis
    }
    range = axis.get_view_interval()

    def is_right_axis(xaxis):
        # there could be no ticks
        # assert xaxis.get_ticks_position() == xaxis.get_label_position()
        return xaxis.get_label_position() == 'right'

    def is_left_axis(yaxis):
        # assert yaxis.get_ticks_position() == yaxis.get_label_position()
        return yaxis.get_label_position() == 'left'

    def is_top_axis(xaxis):
        # assert xaxis.get_ticks_position() == xaxis.get_label_position()
        return xaxis.get_label_position() == 'top'

    def is_bottom_axis(xaxis):
        # assert xaxis.get_ticks_position() == xaxis.get_label_position()
        return xaxis.get_label_position() == 'bottom'

    tag_map_cart2d = {
        'right' : is_right_axis,
        'left'  : is_left_axis,
        'top'   : is_top_axis,
        'bottom': is_bottom_axis
    }

    def is_clockwise_axis(angular_axis):
        return angular_axis.get_theta_direction() == 1

    def is_counterclockwise_axis(angular_axis):
        return angular_axis.get_theta_direction() == -1

    tag_map_angular = {
        'clockwise'       : is_clockwise_axis,
        'counterclockwise': is_counterclockwise_axis
    }

    def assign_tag(axis):
        if type(axis) in [maxis.XAxis, maxis.YAxis]:  # for XAxis3D, YAxis3D this is False
            map = tag_map_cart2d
        elif type(axis) == mpolar.ThetaAxis:
            map = tag_map_angular
        else:
            return None

        for tag, func in map.items():
            if func(axis) is True:
                return tag

        raise RuntimeError('Unrecognized axis ' + str(axis))

    a = subplot_cls_name_mapping[type(axis)](info=assign_tag(axis), range=tuple(round_float(range)),
                                             tick_labels=[convert_text(label, include_position=False) for label in
                                                          axis.get_ticklabels()],
                                             tick_locations=round_float([val for val in axis.get_ticklocs()]))

    if axis.get_label().get_text():
        a.label = convert_text(axis.get_label(), include_position=False)

    return a


def convert_legend(legend):
    """ #TODO """

    def convert_entry(entry):
        if isinstance(entry, mcollections.PathCollection):
            return match_marker(entry.get_paths()[0])(size=entry.get_sizes(),
                                                      color=entry.get_facecolor())

        if isinstance(entry, matplotlib.patches.Rectangle):
            return Polygon(edge_color=entry.get_edgecolor(),
                           face_color=entry.get_facecolor())

        if isinstance(entry, matplotlib.lines.Line2D):
            return Segment(color=entry.get_color(),
                           style=entry.get_linestyle(),
                           width=entry.get_linewidth())

        return

    return Legend(glyphs=[convert_entry(handle) for handle in legend.legendHandles],
                  labels=[convert_text(text, include_position=False) for text in legend.texts])


def convert_colorbar(colorbar):
    cmap = colorbar.cmap
    return Colorbar(title=colorbar._label,
                    tick_vals=colorbar.get_ticks(),
                    bar_range=(colorbar.vmin, colorbar.vmax),
                    colormap=cmap_to_uhe(cmap))


def convert_text(text, include_position=False):
    assert isinstance(text, matplotlib.text.Text)

    if include_position is False:
        return Text(text.get_text(),
                    font_size=text.get_fontsize(),
                    font_name=text.get_fontname(),
                    font_style=text.get_fontstyle(),
                    text_color=text.get_color())
    else:
        return Annotation(round_float(text.get_position()),
                          text.get_text(),
                          font_size=text.get_fontsize(),
                          font_name=text.get_fontname(),
                          font_style=text.get_fontstyle(),
                          text_color=text.get_color())


ls_mapper = {_get_dash_pattern(linestyle_symbol): style_name
             for linestyle_symbol, style_name in matplotlib.lines.ls_mapper.items()}


def convert_linestyle(us_dashOffset_seq):
    """
    Args
        (Unscaled dashoffset:float, sequence of segment of dash:tuple float)
    """

    return ls_mapper[us_dashOffset_seq].upper()


path_vertices_to_marker_symbol = {}
for symbol, name in matplotlib.markers.MarkerStyle.markers.items():
    marker_obj = matplotlib.markers.MarkerStyle(symbol)
    path = marker_obj.get_path().transformed(marker_obj.get_transform())
    path_vertices_to_marker_symbol[totuple(path.vertices.tolist())] = symbol
marker_symbol_to_uhe_style = {
    'o': DiscPoint
}


def match_marker(path):
    """
    marker parameters, (e.g. 'o') are saved as Path
    this method convert Path object to UHE style

    #TODO table of matching here
    """
    vertices = totuple(path.vertices.tolist())

    return marker_symbol_to_uhe_style[path_vertices_to_marker_symbol[vertices]]


def convert_color(c):
    """
    Name color -> CSS color or RGB255
    Unnamed color -> RGB255
    """

    from color_colormap import color_name_to_css_name

    if isinstance(c, str) and c[0] != '#':
        c = c.lower()
        if c in color_name_to_css_name:
            return NamedColor(color_name_to_css_name[c])

    r, g, b = mcolors.to_rgb(c)
    return RGB255Color(r * 255, g * 255, b * 255)


def mpl_listed_data_to_uhe(cmap_data):
    """
    Convert a piecewise constant colormap to universal hierarchy representation

    Args:
     cmap: list of colors (R,G,B)

    Returns: UHE colormap (refer to the top of this file)
    """

    colors = np.array(cmap_data)
    row_num, channel_num = colors.shape
    vals = np.linspace(0, 1, row_num + 1)
    scale = np.zeros((2 * row_num))
    scale[0] = vals[0]
    scale[1:-1:2] = vals[1:-1]
    scale[2:-1:2] = vals[1:-1]
    scale[-1] = vals[-1]
    uhe_colors = np.zeros((2 * row_num, channel_num))
    uhe_colors[::2, :] = colors
    uhe_colors[1::2, :] = colors

    colors_clip = np.clip(uhe_colors, 0, 1)
    return NonUniformColormap(np.concatenate((scale.reshape(-1, 1), colors_clip * 255), axis=1))


def mpl_linear_data_to_uhe(cmap_data):
    """
    Convert a piecewise linear gradient colormap to UHE representation

    Args:
     cmap: list of colors (R,G,B)

    Returns: UHE colormap (refer to the top of this file)
    """

    if 'red' in cmap_data:
        def convert_points(discont_points):
            """ convert list of [xi, yi_left, yi_right] to list of [xi, yi] """

            if callable(discont_points):  # GNU palette
                xs = np.linspace(0, 1, 1024)
                ys = discont_points(xs)
                return list(zip(xs, ys))

            old_xs, ys_left, ys_right = zip(*discont_points)
            ys_left = np.array(ys_left)
            ys_right = np.array(ys_right)
            ys_left[ys_left != ys_right] -= EPSILON
            ys_right[ys_left != ys_right] += EPSILON
            xs = np.zeros(len(old_xs) * 2)
            xs[::2], xs[1::2] = old_xs, old_xs
            ys = np.zeros(len(ys_left) * 2)
            ys[::2], ys[1::2] = ys_left, ys_right
            new_points = np.array(list(zip(xs, ys)))
            rep = []
            for i in range(1, len(new_points)):
                if np.array_equal(new_points[i - 1], new_points[i]):
                    rep.append(i)
            new_points = np.delete(new_points, rep, axis=0)

            return new_points

        red_x, red_y = zip(*convert_points(cmap_data['red']))
        blue_x, blue_y = zip(*convert_points(cmap_data['blue']))
        green_x, green_y = zip(*convert_points(cmap_data['green']))
        red_func = lambda x: float(scipy.interpolate.interp1d(red_x, red_y, kind='linear')(x))
        blue_func = lambda x: float(scipy.interpolate.interp1d(blue_x, blue_y, kind='linear')(x))
        green_func = lambda x: float(scipy.interpolate.interp1d(green_x, green_y, kind='linear')(x))

        colors = []
        xs = sorted(list({*red_x, *blue_x, *green_x}))
        xi, ri, gi, bi = 0, 0, 0, 0
        while xi < len(xs):
            if ri < len(red_x) and red_x[ri] == xs[xi]:
                r = red_y[ri]
                ri += 1
            else:
                r = red_func(xs[xi])

            if gi < len(green_x) and green_x[gi] == xs[xi]:
                g = green_y[gi]
                gi += 1
            else:
                g = green_func(xs[xi])

            if bi < len(blue_x) and blue_x[bi] == xs[xi]:
                b = blue_y[bi]
                bi += 1
            else:
                b = blue_func(xs[xi])

            colors.append([xs[xi], r, g, b])
            if (ri == len(red_x) or red_x[ri] > xs[xi]) \
                    and (gi == len(green_x) or green_x[gi] > xs[xi]) \
                    and (bi == len(blue_x) or blue_x[bi] > xs[xi]):
                xi += 1

        colors = np.array(colors)
        colors[:, 1:] = np.clip(colors[:, 1:], 0, 1) * 255

        return UniformColormap(colors)
    else:
        if isinstance(cmap_data, tuple) and isinstance(cmap_data[0][1], tuple):
            vals, colors = zip(*cmap_data)
            vals = np.array(vals).reshape(-1, 1)
            colors = np.array(colors)
        else:
            vals = np.linspace(0, 1, len(cmap_data)).reshape(-1, 1)
            colors = np.array(cmap_data)

        return NonUniformColormap(np.concatenate((vals, np.clip(colors, 0, 1) * 255), axis=1))


def cmap_to_uhe(cmap):
    """
    Convert a custom Matplotlib colormap object to UHE representation

    Args:
     cmap: Matplotlib colormap object

    Returns: UHE colormap (refer to the top of this file)
    """

    if cmap.name is not None:
        return 'matplotlib-' + cmap.name.lower()

    if hasattr(cmap, '_segmentdata'):
        return mpl_linear_data_to_uhe(cmap._segmentdata)
    else:
        assert hasattr(cmap, 'colors')
        return mpl_listed_data_to_uhe(cmap.name)


def uhe_to_mpl_ls(cmap, name=None):
    """ Convert a UHE colormap to Matplotlib LinearSegmented colormap """

    val = cmap[:, 0]
    colors = cmap[:, 1:] / 255
    cmap_list = list(zip(val, colors))
    return mcolors.LinearSegmentedColormap.from_list(colors=cmap_list, name=name)
