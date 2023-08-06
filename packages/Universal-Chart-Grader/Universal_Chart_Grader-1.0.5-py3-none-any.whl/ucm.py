## --- Elements ---
import io
from enum import Enum
from typing import List, Mapping, Tuple

import numpy as np
import pyprnt
from matplotlib import rcParams
from matplotlib.colors import to_rgb

null_objs = [None, [], tuple()]


class Element(Mapping):
    def items(self):
        for k, v in self.__dict__.items():
            if isinstance(v, np.ndarray):
                if len(v) > 0:
                    yield k, v
            elif v not in null_objs:
                yield k, v

    def keys(self):
        for k, v in self.__dict__.items():
            if isinstance(v, np.ndarray):
                if len(v) > 0:
                    yield k
            elif v not in null_objs:
                yield k

    def values(self):
        for k, v in self.__dict__.items():
            if isinstance(v, np.ndarray):
                if len(v) > 0:
                    yield v

            elif v not in null_objs:
                yield v

    def __len__(self):
        return len({k: v for k, v in self.__dict__.items() if v is not None})

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __iter__(self):
        return self.__dict__.__iter__()

    def __repr__(self):
        sio = io.StringIO()
        pyprnt.prnt(self, file=sio)
        return sio.getvalue()

        # d = {k: v for k, v in self.__dict__.items() if v is not None}
        # return repr(d)


class Basic(Element):
    pass


## --- Basic Elements ---

class Text(Basic):
    def __init__(self, text,
                 font_size=None,
                 font_name=None,
                 font_style=None,
                 text_color=None):
        self.text = text
        self.font_size = font_size if font_size != rcParams['font.size'] else None
        self.font_name = font_name if font_name != 'DejaVu Sans' else None
        self.font_style = font_style if font_style != rcParams['font.style'] else None
        self.text_color = text_color if text_color != rcParams['text.color'] else None


class Color(Basic):
    def toRGB255(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.toRGB255() == other.toRGB255()
        return False

    def __lt__(self, other):
        if isinstance(other, Color):
            return self.toRGB255() < other.toRGB255()
        return False


class NamedColor(Color):
    def __init__(self, name):
        self.name = name

    def toRGB255(self):
        r, g, b = np.array(to_rgb(self.name)) * 255
        return int(r), int(g), int(b)


class RGB255Color(Color):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def toRGB255(self):
        return self.r, self.g, self.b


class Colormap(Basic):
    pass


class NamedColormap(Colormap):
    def __init__(self, name):
        super().__init__()
        self.info = name


class UniformColormap(Colormap):
    def __init__(self, colors):
        self.info = colors


class NonUniformColormap(Colormap):
    def __init__(self, val_colors):
        self.val_colors = val_colors


## --- Marker Elements ---

class Marker(Element):
    def __lt__(self, other):
        if type(self) == type(other):
            return tuple(self.values()) < tuple(other.values())
        assert isinstance(other, Marker)
        return tuple(self.keys()) < tuple(other.keys())


class Shading(Enum):
    FLAT = 0
    SMOOTH = 1


class Polygon(Marker):
    def __init__(self, edge_color: Color = None, face_color: Color = None, edge_width=None, shading=None, opacity=None):
        """
        Args:
            edge_color: COLOR
            face_color: COLOR
            edge_width: integer
            shading: enum Shading {FLAT, SMOOTH}
            opacity: float [0..1]
        """

        self.edge_color = edge_color
        self.face_color = face_color
        self.edge_width = edge_width
        self.shading = shading
        self.opacity = opacity


class SegmentStyle:
    SOLID = 0
    DASHED = 1
    DOTTED = 2
    DASHEDDOTTED = 3


class Segment(Marker):
    def __init__(self, color: Color = None, width: int = None, style: SegmentStyle = None):
        self.color = color
        self.width = width
        self.style = style


class Point(Marker):
    def __init__(self, color=None):
        self.color = color


class DiscPoint(Point):
    def __init__(self, color=None, size: float = None):
        """
        Args:
            color: Color
            size: float denoting radius
        """
        super().__init__(color)
        self.size = size


class CrossPoint(Point):
    def __init__(self, color=None):
        super().__init__(color)
        self.size = None


class EllipsePoint(Point):
    def __init__(self, color=None, size: Tuple[float] = None):
        """
        Args:
            color: Color
            size: Pair of float, major axis length, minor axis length
        """
        super().__init__(color)
        self.size = size


class RectanglePoint(Point):
    def __init__(self, color=None, size: Tuple[float] = None):
        """
        Args:
            color: Color
            size: Pair of float (width, height)
        """
        super().__init__(color)
        self.size = size


## --- Guides ---

class Guide(Element):
    pass


class Axis(Guide):
    def __init__(self, label=None, range=None, tick_locs=None, tick_labels=None):
        self.label = label
        self.range = range
        self.tick_locations = tick_locs
        self.tick_labels = tick_labels

    def __lt__(self, other):
        return self.type < other.type


class XAxisPos(Enum):
    LEFT = 'Left'
    RIGHT = 'Right'


class XAxis(Axis):
    type = 'X'

    def __init__(self, info: XAxisPos, label=None, range=None, tick_locations=None, tick_labels=None):
        super().__init__(label, range, tick_locations, tick_labels)
        self.info = info
        self.type = XAxis.type


class YAxisPos(Enum):
    TOP = 'Top'
    BOTTOM = 'Bottom'


class YAxis(Axis):
    type = 'Y'

    def __init__(self, info: YAxisPos, label=None, range=None, tick_locations=None, tick_labels=None):
        super().__init__(label, range, tick_locations, tick_labels)
        self.info = info
        self.type = YAxis.type


class ZAxisPos(Enum):
    LOWER_LEFT = 'Lower left'
    LOWER_RIGHT = 'Lower right'
    UPPER_LEFT = 'Upper left'
    UPPER_RIGHT = 'Upper right'


class ZAxis(Axis):
    type = 'Z'

    def __init__(self, info: ZAxisPos, label=None, range=None, tick_locs=None, tick_labels=None):
        super().__init__(label, range, tick_locs, tick_labels)
        self.info = info
        self.type = ZAxis.type


class RadialAxis(Axis):
    type = 'Radius'

    def __init__(self, info: float, label=None, range=None, tick_locs=None, tick_labels=None):
        super().__init__(label, range, tick_locs, tick_labels)
        self.info = info
        self.type = RadialAxis.type


class AngularAxisDirection(Enum):
    CLOCKWISE = 'Clockwise'
    COUNTERCLOCKWISE = 'Counter-Clockwise'


class AngularAxis(Axis):
    type = 'Angle'

    def __init__(self, info: AngularAxisDirection, label=None, range=None, tick_locs=None, tick_labels=None):
        super().__init__(label, range, tick_locs, tick_labels)
        self.info = info
        self.type = AngularAxis.type


class Legend(Guide):
    def __init__(self, glyphs: List[Marker], labels: List[Text], title: Text = None):
        self.glyphs = glyphs
        self.labels = labels
        self.title = title


class Colorbar(Guide):
    def __init__(self, tick_vals: List[float], bar_range: Tuple[float, float], colormap: [Colormap], title=None):
        self.tick_vals = tick_vals
        self.bar_range = bar_range
        self.colormap = colormap
        self.title = title


class Annotation(Guide, Text):
    def __init__(self, pos, text, font_size=None, font_name=None, font_style=None, text_color=None):
        super().__init__(text, font_size, font_name, font_style, text_color)
        self.pos = pos


class Graphic(Element):
    def __init__(self, axes=None, label: str = None, zorder=None):
        self.axes = axes
        self.label = label
        self.zorder = zorder


## --- Graphics ---

class Mesh(Graphic):
    def __init__(self, positions, topology=None, axes=None, label: str = None, zorder=None):
        super().__init__(axes, label, zorder)
        self.positions = tuple(map(tuple, positions))
        self.topology = topology if topology is not None else []

    def __lt__(self, other):
        keys = ['type', 'axes', 'zorder', 'positions', 'topology']
        for key in keys:
            this_key = getattr(self, key)
            that_key = getattr(other, key)
            if this_key == that_key:
                continue
            elif this_key < that_key:
                return True
            else:
                return False
        return False


class Scatter(Mesh):
    type = 'Scatter'

    def __init__(self, positions, topology=None, axes=None, label: str = None, zorder=None):
        super().__init__(positions, topology, axes, label, zorder)
        self.type = Scatter.type


class Line2D(Mesh):
    type = 'Line2D'

    def __init__(self, positions, topology=None, axes=None, label: str = None, zorder=None):
        super().__init__(positions, topology, axes, label, zorder)
        self.type = Line2D.type


class Line3D(Mesh):
    type = 'Line3D'

    def __init__(self, positions, topology=None, axes=None, label: str = None, zorder=None):
        super().__init__(positions, topology, axes, label, zorder)
        self.type = Line3D.type



class Network(Mesh):
    type = 'Network'

    def __init__(self, positions, topology=None, axes=None, label: str = None, zorder=None):
        super().__init__(positions, topology, axes, label, zorder)
        self.type = Network.type


class PolyMesh(Mesh):
    type = 'PolyMesh'

    def __init__(self, positions, topology=None, axes=None, label: str = None, zorder=None):
        super().__init__(positions, topology, axes, label, zorder)
        self.type = PolyMesh.type



class Grid(Graphic):
    def __init__(self, vals, value_range, extents, colormap: Colormap, axes=None, label: str = None, zorder=None):
        super().__init__(axes, label, zorder)
        self.vals = vals
        self.value_range = value_range
        self.colormap = colormap
        self.extents = extents


class Image2D(Grid):
    type = 'Image2D'

    def __init__(self, vals, value_range, extents, colormap: Colormap):
        super().__init__(vals, value_range, extents, colormap)
        self.type = Image2D.type


class Image3D(Grid):
    type = 'Image3D'

    def __init__(self, vals, value_range, extents, colormap: Colormap):
        super().__init__(vals, value_range, extents, colormap)
        self.type = Image3D.type


class Height3D(Grid):
    type = 'Height3D'

    def __init__(self, vals, value_range, extents, colormap: Colormap):
        super().__init__(vals, value_range, extents, colormap)
        self.type = Height3D.type


## --- Layout ---

class Layout(Element):
    pass


class Figure(Layout):
    def __init__(self, legends=None, subplots=None, size=None, title=None):
        self.size = size
        self.title = title
        self.legends = legends
        self.subplots = subplots


class Coord_Sys(Enum):
    CARTESIAN_2D = 'Cartesian 2D'
    CARTESIAN_3D = 'Cartesian 3D'
    POLAR_2D = 'Polar'

    def __repr__(self):
        return str(self.value)


class Subplot(Layout):
    def __init__(self, pos, title=None, display_range=None, coordinates_system=None, axes=None, legends=None,
                 colorbars=None, annotations=None, grids=None,
                 meshes=None):
        self.pos = pos
        self.title = title
        self.display_range = display_range
        self.coordinates_system = coordinates_system
        self.axes = axes
        self.legends = legends
        self.colorbars = colorbars
        self.annotations = annotations
        self.grids = grids
        self.meshes = meshes