import datetime
import inspect
import itertools
import re
import tempfile
from abc import ABC

import matplotlib.dates as mdates
import numpy as np
import plotly.graph_objects as go
import plotly.io, plotly.colors

from .plotly_browser_adapter_old import BrowserFigure, start_browser
from .utils import cast_float, rad_2pi

null_objs = [[], dict(), tuple(), None]


def is_null_obj(obj):
    if isinstance(obj, np.ndarray):
        return False
    return obj in null_objs


ROUND_DIGIT = 2


def add_attribute(d, key, val, filter):
    if filter(key, val):
        return
    d[key] = val


def meta_add_attribute(d, filter=lambda key, val: is_null_obj(val)):
    def wrapper(key, val):
        add_attribute(d, key, val, filter)

    return wrapper


def plotly_convert(fig):
    html = plotly.io.to_html(fig)
    with tempfile.TemporaryDirectory() as dirpath:
        path = dirpath + 'plotly_py_output.html'
        with open(path, 'w') as html_file:
            html_file.write(html)
        browser = start_browser("file://" + path)

    try:
        bfig = BrowserFigure(browser)
        ff = FigureFacade(fig, bfig)
        ucm = ff.export()
    finally:
        bfig.browser.close()

    return ucm

def convert_text(pltly_text):
    assert pltly_text is not None

    if isinstance(pltly_text, str):
        return dict(text=pltly_text)

    font = pltly_text['font']

    d = {}
    add_attribute = meta_add_attribute(d)
    add_attribute('text', pltly_text['text'])
    add_attribute('family', font['family'])
    add_attribute('fontsize', font['size'])
    add_attribute('color', font['color'])
    return d


class FigureFacade:
    def __init__(self, fig, browser_fig: BrowserFigure):
        self.fig = fig
        self.browser_fig = browser_fig

    def width(self):
        return self.browser_fig.figure_width()

    def height(self):
        return self.browser_fig.figure_height()

    def title(self):
        tt = self.fig.layout.title
        if tt is not None:
            return convert_text(tt)

    def subplots(self):
        l = []

        if self.fig._grid_ref is None:
            if any('3d' in type(trace).__name__.lower() for trace in self.fig.data):  # 3D cartesian
                l.append(Cartesian3DSubplot(self.fig, self.browser_fig, row=0, col=0, scene_key='scene'))
            elif any('polar' in type(trace).__name__.lower() for trace in self.fig.data):  # polar
                l.append(PolarSubplot(self.fig, self.browser_fig, row=0, col=0, polar_key='polar'))
            else:
                # 2d cartesian
                l.append(Cartesian2DSubplot(self.fig, self.browser_fig, row=0, col=0, x_key='xaxis', y_key='yaxis'))

        else:
            rows = len(self.fig._grid_ref)
            cols = len(self.fig._grid_ref[0])

            for i, j in itertools.product(range(rows), range(cols)):
                subplot_spec = self.fig._grid_ref[i][j][0]
                subplot_type = subplot_spec.subplot_type
                if subplot_type == 'xy':
                    l.append(
                            Cartesian2DSubplot(self.fig, self.browser_fig, i, j,
                                               *subplot_spec.layout_keys))  # 2d cartesian
                elif subplot_type == 'scene':
                    l.append(
                            Cartesian3DSubplot(self.fig, self.browser_fig, i, j,
                                               *subplot_spec.layout_keys))  # 3d cartesian
                elif subplot_type == 'polar':
                    l.append(PolarSubplot(self.fig, self.browser_fig, i, j, *subplot_spec.layout_keys))  # polar
                else:
                    raise NotImplementedError('Unexpected subplot type')

        return [subplot.export() for subplot in l]

    def axes(self):
        return []

    def export(self):
        d = {}
        add_attribute = meta_add_attribute(d)
        add_attribute('size', (self.width(), self.height()))
        add_attribute('title', self.title())
        add_attribute('subplots', self.subplots())
        add_attribute('axes', self.axes())
        return d


def scatterTraceSize(trace):
    if trace.x is not None:
        return len(trace.x)
    elif trace.y is not None:
        return len(trace.y)
    elif trace.theta is not None:
        raise RuntimeError('Invalid scatter trace')


class PlaceHolder:
    def __init__(self, key, val):
        self.key = key
        self.val = val


class Cart2DTraceFacade:
    def axes(self):
        d = []
        if self.trace.xaxis is not None:
            d.append(PlaceHolder('axis_name_to_guide_idx', self.trace.xaxis))
        else:
            d.append(PlaceHolder('axis_name_to_guide_idx', 'x'))

        if self.trace.yaxis is not None:
            d.append(PlaceHolder('axis_name_to_guide_idx', self.trace.yaxis))
        else:
            d.append(PlaceHolder('axis_name_to_guide_idx', 'y'))

        return d


class ScatterFacade(Cart2DTraceFacade):
    def __init__(self, trace):
        self.trace = trace
        self.trace_x = cast_float(trace.x) if trace.x is not None else list(range(len(trace.y)))
        self.trace_y = cast_float(trace.y) if trace.y is not None else list(range(len(trace.x)))

    def export(self):
        return {
            'points': np.array(list(sorted(list(zip(self.trace_x, self.trace_y))))),
            'axes'  : [axis for axis in self.axes()]
        }


class LineFacade(Cart2DTraceFacade):
    def __init__(self, trace):
        self.trace = trace
        self.trace_x = cast_float(trace.x) if trace.x is not None else list(range(len(trace.y)))
        self.trace_y = cast_float(trace.y) if trace.y is not None else list(range(len(trace.x)))

    def export(self):
        return {
            'grid': np.array(list(zip(self.trace_x, self.trace_y))),
            'axes': [axis for axis in self.axes()]
        }


class PolarScatterFacade:
    def __init__(self, trace):
        self.trace = trace

    def export(self):
        r = self.trace.r if self.trace.r is not None else list(range(len(self.trace.theta)))
        theta = self.trace.theta if self.trace.theta is not None else np.linspace(0, 360, len(self.trace.r))
        theta = [rad_2pi(theta) for theta in np.deg2rad(theta)]

        return {
            'points'  : np.array(list(zip(r, theta))),
            'topology': [],
            'axes'    : [0, 1]  # TODO
        }


class PolarLineFacade:
    def __init__(self, trace):
        self.trace = trace

    def export(self):
        r = self.trace.r if self.trace.r is not None else list(range(len(self.trace.theta)))
        theta = self.trace.theta if self.trace.theta is not None else np.linspace(0, 360, len(self.trace.r))
        theta = [rad_2pi(theta) for theta in np.deg2rad(theta)]

        return {
            'grid': np.array(list(zip(r, theta))),
            'axes': [0, 1]  # TODO
        }


def pltly_scatter_mode(trace):
    """
    Args:
        trace: go.Scatter

    Returns:
        boolean value, input trace is displayed as scatter or not
    """

    assert isinstance(trace, (go.Scatter, go.Scatter3d))

    if trace.x is not None:
        n = len(trace.x)
    elif trace.y is not None:
        n = len(trace.y)
    elif hasattr(trace, 'z') and trace.z is not None:
        n = len(trace.z)
    else:
        raise RuntimeError('Invalid scatter trace')

    if trace.mode is None and n < 20:
        return 'markers+lines'
    elif trace.mode is None:
        return 'lines'
    else:
        return trace.mode


def pltly_scatterpolar_mode(trace):
    """
    Args:
        trace: go.Scatterpolar

    Returns:
        boolean value, input trace is displayed as scatter or not
    """

    assert isinstance(trace, go.Scatterpolar)

    if trace.theta is not None:
        n = len(trace.theta)
    elif trace.r is not None:
        n = len(trace.r)
    else:
        raise RuntimeError('Invalid scatter trace')

    if trace.mode is None and n < 20:
        return 'markers+lines'
    elif trace.mode is None:
        return 'lines'
    else:
        return trace.mode


def isCartScatter(trace):
    """ Is UHE Scatter-like """
    return isinstance(trace, go.Scatter) and 'markers' in pltly_scatter_mode(trace)


def isCartLine(trace):
    """ Is UHE line-like """
    return isinstance(trace, go.Scatter) and 'lines' in pltly_scatter_mode(trace)


def isPolarScatter(trace):
    """ Is UHE Scatter-like """
    return isinstance(trace, go.Scatterpolar) and 'markers' in pltly_scatterpolar_mode(trace)


def isPolarLine(trace):
    """ Is UHE line-like """
    return isinstance(trace, go.Scatterpolar) and 'lines' in pltly_scatterpolar_mode(trace)


mesh_trace_filters = [isCartScatter, isPolarScatter]
grid_trace_filters = [isCartLine, isPolarLine]
facade_mapper = {isCartScatter : ScatterFacade, isCartLine: LineFacade,
                 isPolarScatter: PolarScatterFacade, isPolarLine: PolarLineFacade}


def createFacade(trace):
    for f, factory in facade_mapper.items():
        if f(trace):
            return factory(trace)
    raise RuntimeError('Unexpected trace type')


isMeshTrace = lambda trace: any(f(trace) for f in mesh_trace_filters)
isGridTrace = lambda trace: any(f(trace) for f in grid_trace_filters)


def fill_placeholder(axis_key_map, graphic):
    for i in range(len(graphic['axes'])):
        obj = graphic['axes'][i]
        if isinstance(obj, PlaceHolder):
            if obj.key == 'axis_name_to_guide_idx':
                graphic['axes'][i] = axis_key_map[obj.val]
    return graphic


class SubplotFacade:
    def __init__(self, fig, browser_fig: BrowserFigure, row, col):
        self.fig = fig
        self.browser_fig = browser_fig
        self._row = row
        self._col = col
        self.axis_key_map = {}

    def row(self):
        return self._row

    def col(self):
        return self._col

    def coord_system(self):
        raise NotImplementedError()

    def display_aspect_ratio(self):
        raise NotImplementedError()

    def axes(self):
        raise NotImplementedError()

    def colorbars(self):
        raise NotImplementedError()

    def legends(self):
        raise NotImplementedError()

    def meshes(self):
        mesh_list = []
        for trace in self.fig.data:
            if trace not in self:
                continue

            if isMeshTrace(trace):
                mesh_list.append(createFacade(trace).export())

        return mesh_list

    def grids(self):
        grid_list = []
        for trace in self.fig.data:
            if trace not in self:
                continue

            if isGridTrace(trace):
                grid_list.append(createFacade(trace).export())

        return grid_list

    def export(self):
        d = {}
        add_attribute = meta_add_attribute(d)
        add_attribute('(row, col)', (self._row, self._col))
        add_attribute('coordinate system', self.coord_system())
        add_attribute('display aspect ratio', np.round_(self.display_aspect_ratio(), ROUND_DIGIT))
        add_attribute('axes', self.axes())
        add_attribute('colorbars', self.colorbars())
        add_attribute('legends', self.legends())
        add_attribute('grids', [fill_placeholder(self.axis_key_map, grid) for grid in self.grids()])
        add_attribute('meshes', [fill_placeholder(self.axis_key_map, mesh) for mesh in self.meshes()])
        return d

    def __contains__(self, trace):
        raise NotImplementedError()

    def _axes_indices(self, trace):
        raise NotImplementedError()


def key_to_val(key):
    return key.replace('axis', '')


def val_to_key(val):
    return val[0] + 'axis' + val[1:]


def axis_equiv(fig, x_val1, x_val2):
    if x_val1 == x_val2:
        return True
    else:
        if fig._grid_ref is None:
            return True

        x_key1, x_key2 = val_to_key(x_val1), val_to_key(x_val2)

        while True:
            next_val = fig.layout[x_key1].overlaying
            if next_val == x_val2:
                return True
            else:
                x_key1 = val_to_key(next_val)
            if next_val is None:
                break

        while True:
            next_val = fig.layout[x_key2].overlaying
            if next_val == x_val1:
                return True
            else:
                x_key2 = val_to_key(next_val)
            if next_val is None:
                break

        return False


class Cartesian2DSubplot(SubplotFacade, ABC):
    def __init__(self, fig, browser_fig, row, col, x_key, y_key):
        super().__init__(fig, browser_fig, row, col)
        self.x_key = x_key
        self.y_key = y_key
        self.x_val = self.x_key.replace('axis', '')
        self.y_val = self.y_key.replace('axis', '')

    def coord_system(self):
        return 'Cartesian 2D'

    def axes(self):
        def is_twinx(axis_key):
            return axis_equiv(self.fig, key_to_val(axis_key), self.x_key)

        def is_twiny(axis_key):
            return axis_equiv(self.fig, key_to_val(axis_key), self.y_key)

        axis_keys = [self.x_key, self.y_key] + \
                    [key for key, val in self.fig.layout._compound_props.items()
                     if 'axis' in key and key != self.x_key and key != self.y_key and (is_twinx(key) or is_twiny(key))]

        axes = []
        for idx, axis_key in enumerate(axis_keys):
            d = {}
            self.axis_key_map[axis_key.replace('axis', '')] = idx
            add_attribute = meta_add_attribute(d)
            add_attribute('type', axis_key[0])
            range = self.browser_fig.cart2d_axis_attr(axis_key, 'range')
            axis_type = self.browser_fig.cart2d_axis_attr(axis_key, 'type')
            tickvals = self.browser_fig.cart2d_tick_vals(axis_key)
            tick_font = {}
            if self.fig.layout[axis_key].info is not None:
                tick_font['color'] = self.fig.layout[axis_key].info
            if hasattr(self.fig.layout[axis_key], 'tickfont'):
                tick_font.update(self.fig.layout[axis_key]['tickfont']._compound_props)
            if tickvals is None:
                tickvals = self.browser_fig.cart2d_tick_vals_tickvals(axis_key)
            if axis_type == 'linear':
                add_attribute('range', tuple(np.round_(range, ROUND_DIGIT)))
                add_attribute('tick locations', np.round_(tickvals, ROUND_DIGIT))
            elif axis_type == 'date':
                add_attribute('range',
                              [mdates.date2num(datetime.datetime.strptime(date, '%Y-%m-%d')) for date in range])
                add_attribute('tick locations',
                              [mdates.date2num(datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')) for dt in tickvals])
            add_attribute('tick labels', [{'text': text, **tick_font} for text in
                                          self.browser_fig.cart2d_tick_labels(axis_key)])  # TODO
            tt = self.fig.layout[axis_key].title
            if tt is not None:
                label = {}
                add_to_label = meta_add_attribute(label)
                add_to_label('color', self.fig.layout[axis_key]['color'])
                label.update(convert_text(tt))
                add_attribute('label', label)
            axes.append(d)

        return [axis for axis in axes if axis not in null_objs]

    def colorbars(self):
        return []  # TODO

    def legends(self):
        return []  # TODO

    def display_aspect_ratio(self):
        x0, x1 = self.browser_fig.cart2d_axis_attr(self.x_key, 'domain')
        y0, y1 = self.browser_fig.cart2d_axis_attr(self.y_key, 'domain')
        fig_width = self.browser_fig.figure_width()
        fig_height = self.browser_fig.figure_height()
        return (y1 - y0) * fig_height / ((x1 - x0) * fig_width)

    def __contains__(self, trace):
        trace_xaxis = trace.xaxis if hasattr(trace, 'xaxis') else 'x'
        trace_yaxis = trace.yaxis if hasattr(trace, 'yaxis') else 'y'

        return axis_equiv(self.fig, trace_xaxis, self.x_val) and axis_equiv(self.fig, trace_yaxis, self.y_val)


class Cartesian3DSubplot(SubplotFacade):
    def __init__(self, fig, browser_fig, row, col, scene_key):
        super().__init__(fig, browser_fig, row, col)
        self.scene_key = scene_key

    def coord_system(self):
        return 'Cartesian 3D'

    def xaxis(self):
        d = {}
        add_attribute = meta_add_attribute(d)
        add_attribute('type', 'x')
        add_attribute('range',
                      tuple(np.round_(self.browser_fig.cart3d_xaxis_attr(self.scene_key, 'range'), ROUND_DIGIT)))
        add_attribute('tick labels', [])
        add_attribute('tick locations', [])
        tt = self.fig.layout[self.scene_key]['xaxis']['title']
        if tt is not None:
            label = {}
            add_to_label = meta_add_attribute(label)
            add_to_label('color', self.fig.layout[self.scene_key]['xaxis']['color'])
            label.update(convert_text(tt))
            add_attribute('label', label)

        return d

    def yaxis(self):
        d = {}
        add_attribute = meta_add_attribute(d)
        add_attribute('type', 'y')
        add_attribute('range',
                      tuple(np.round_(self.browser_fig.cart3d_yaxis_attr(self.scene_key, 'range'), ROUND_DIGIT)))
        add_attribute('tick labels', [])
        add_attribute('tick locations', [])
        tt = self.fig.layout[self.scene_key]['yaxis']['title']
        if tt is not None:
            label = {}
            add_to_label = meta_add_attribute(label)
            add_to_label('color', self.fig.layout[self.scene_key]['yaxis']['color'])
            label.update(convert_text(tt))
            add_attribute('label', label)
        return d

    def zaxis(self):
        d = {}
        add_attribute = meta_add_attribute(d)
        add_attribute('type', 'z')
        add_attribute('range',
                      tuple(np.round_(self.browser_fig.cart3d_zaxis_attr(self.scene_key, 'range'), ROUND_DIGIT)))
        add_attribute('tick labels', [])
        add_attribute('tick locations', [])
        tt = self.fig.layout[self.scene_key]['zaxis']['title']
        if tt is not None:
            label = {}
            add_to_label = meta_add_attribute(label)
            add_to_label('color', self.fig.layout[self.scene_key]['zaxis']['color'])
            label.update(convert_text(tt))
            add_attribute('label', label)
        return d

    def display_aspect_ratio(self):
        d = self.browser_fig.scene_attr(self.scene_key, 'domain')
        x0, x1 = d['x']
        y0, y1 = d['y']
        return (y1 - y0) / (x1 - x0)

    def colorbars(self):
        return []  # TODO

    def legends(self):
        return []  # TODO

    def axes(self):
        return [self.xaxis(), self.yaxis(), self.zaxis()]

    def __contains__(self, trace):
        trace_scene = trace.scene if hasattr(trace, 'scene') else 'scene'
        return trace_scene == self.scene_key


class PolarSubplot(SubplotFacade):
    def __init__(self, fig, fig_browser, row, col, polar_key):
        super().__init__(fig, fig_browser, row, col)
        self.polar_key = polar_key

    def coord_system(self):
        return 'Cartesian 3D'

    def display_aspect_ratio(self):
        d = self.browser_fig.polar_attr(self.polar_key, 'domain')
        x0, x1 = d['x']
        y0, y1 = d['y']
        return (y1 - y0) / (x1 - x0)

    def radial_axis(self):
        d = {}
        add_attribute = meta_add_attribute(d)
        add_attribute('type', 'radial')
        add_attribute('range', tuple(np.round_(self.browser_fig.radialaxis_attr(self.polar_key, 'range'), ROUND_DIGIT)))
        add_attribute('tick labels',
                      [{'text': text} for text in self.browser_fig.tick_labels(self.polar_key, 'xtick')])  # TODO
        add_attribute('tick locations', np.round_(self.browser_fig.tick_vals(self.polar_key, 'xtick'), ROUND_DIGIT))
        tt = self.fig.layout[self.polar_key]['radialaxis']['title']
        if tt is not None:
            add_attribute('label', convert_text(tt))
        return d

    def angular_axis(self):
        d = {}
        add_attribute = meta_add_attribute(d)
        add_attribute('type', 'angular')
        range = self.browser_fig.polar_attr(self.polar_key, 'sector')
        range = np.deg2rad(range)
        add_attribute('range', tuple(np.round_(range, ROUND_DIGIT)))
        add_attribute('tick labels', [{'text': text} for text in
                                      self.browser_fig.tick_labels(self.polar_key, 'angularaxistick')])  # TODO
        add_attribute('tick locations',
                      np.round_(np.deg2rad(self.browser_fig.tick_vals(self.polar_key, 'angularaxistick')), ROUND_DIGIT))
        return d

    def axes(self):
        return [self.radial_axis(), self.angular_axis()]

    def colorbars(self):
        return []  # TODO

    def legends(self):
        return []  # TODO

    def __contains__(self, trace):
        trace_polar = trace.subplot if trace.subplot else 'polar'
        return trace_polar == self.polar_key


def pltly_to_uhe(colorscale):
    """ Convert a Plotly colrscale to UHE """

    if isinstance(colorscale[0], str):
        scale = np.linspace(0, 1, len(colorscale)).reshape(-1, 1)
        colors = colorscale
    else:
        scale = np.array(plotly.colors.colorscale_to_scale(colorscale)).reshape(-1, 1)
        colors = plotly.colors.colorscale_to_colors(colorscale)
    colors, _ = plotly.colors.convert_colors_to_same_type(colors, colortype='rgb')
    colors = [re.match(r'rgb\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)',
                       color.replace(' ', '')).groups()
              for color in colors]
    colors = np.array([[float(r), float(g), float(b)] for r, g, b in colors])

    return np.concatenate((scale, colors), axis=1)


def uhe_to_pltly(cmap):
    """ Convert a UHE colormap to plotly (knot, RGB255 string) """

    colors = cmap[:, 1:].tolist()
    colors = [f'rgb({r}, {g}, {b})' for r, g, b in colors]
    return list(zip(cmap[:, 0], colors))


# Plotly
plotly_cmap_data = {
    c[0].lower(): c[1]
    for c in itertools.chain(
            inspect.getmembers(plotly.colors.sequential),
            inspect.getmembers(plotly.colors.diverging),
            inspect.getmembers(plotly.colors.cyclical))
    if isinstance(c, tuple)
       and len(c) == 2
       and isinstance(c[0], str)
       and isinstance(c[1], list)
       and not c[0].endswith("_r")
       and not c[0].startswith("_")
}

plotly_cmaps = {name.lower(): pltly_to_uhe(cmap_data) for name, cmap_data in plotly_cmap_data.items()}