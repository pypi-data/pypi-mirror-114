import plotly.graph_objs as go
import numpy as np
from plotly.graph_objs import Mesh3d


def plot_trisurf():
    """ Simple triangle surface with vertices labeled """

    VERTS = np.array([[0, 0, -1],
                      [1, 0, 1],
                      [0, 1, 1],
                      [1, 1, 0]])
    TRIS = np.array([(2, 0, 1), (1, 3, 2)])
    mesh3d = go.Mesh3d(x=VERTS[:, 0], y=VERTS[:, 1], z=VERTS[:, 2],
                       i=TRIS[:, 0], j=TRIS[:, 1], k=TRIS[:, 2],
                       intensity=VERTS[:, 2])
    scatter3d = go.Scatter3d(x=VERTS[:,0], y=VERTS[:,1], z=VERTS[:,2],
                             mode='text', text=[n for n in range(len(VERTS))], textfont_size=20)
    fig = go.Figure(data=[mesh3d, scatter3d])
    fig.show()
    return fig


def plotly_stub_convert(fig):
    """
    Stub of plotly_convert()

    Outputs:
    UHE of the input Plotly figure such that:
        - Only the first subplot is converted
        - Only mesh3D traces are converted in this subplot
        - Only 'positions' and 'markers.indices' field appear in the conversion output
    """

    d = {'subplots': [{'meshes': []}]}
    for trace in fig['data']:
        if not isinstance(trace, Mesh3d): continue
        geometry = list(zip(trace['x'], trace['y'], trace['z']))
        topology = list(zip(trace['i'], trace['j'], trace['k']))
        mesh = {'positions': geometry, 'markers': [{'indices': indices} for indices in topology]}
        d['subplots'][0]['meshes'].append(mesh)

    return d

# plotly_stub_convert(plot_trisurf())
