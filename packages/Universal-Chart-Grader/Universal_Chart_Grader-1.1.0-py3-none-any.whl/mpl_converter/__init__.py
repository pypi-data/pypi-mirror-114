import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

from . import monkey_patch
from .matplotlib import mpl_convert
from .matplotlib import mpl_linear_data_to_uhe, mpl_listed_data_to_uhe, uhe_to_mpl_ls


def save_img(fig):
    """ Save an Image that can be evaluated and display in Jupyter notebook """
    import io
    from IPython.display import Image

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return Image(data=buf.getvalue())


def cleanup(fig):
    """  For stateful plotting packages, call this method to clean the states when necessary. """

    import matplotlib.pyplot as plt

    # Close figure
    plt.close(fig)
    plt.clf()