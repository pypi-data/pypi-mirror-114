"""
Monkey-patching Matplotlib for the sake of conversion

This must be imported BEFORE matplotlib.pyplot
"""

import wrapt
@wrapt.patch_function_wrapper('matplotlib.colorbar', 'Colorbar.__init__')
def patch_colorbar_init(wrapped, instance, args, kwargs):
    wrapped(*args, **kwargs)
    instance.ax.__dict__['_is_colorbar'] = True

@wrapt.patch_function_wrapper('matplotlib.figure', 'Figure.colorbar')
def patch_figure_colorbar(wrapped, instance, args, kwargs):
    cb = wrapped(*args, **kwargs)
    if len(args) >= 3:
        ax = args[2]
    elif 'ax' in kwargs:
        ax = kwargs['ax']
    else:
        import matplotlib.pyplot as plt
        ax = plt.gca()

    ax.__colorbar = [cb] if not hasattr(ax, '__colorbar') else ax.__colorbar + [cb]
    return cb

# Note that pyplot also calls this
@wrapt.patch_function_wrapper('matplotlib.axes._axes', 'Axes.contourf')
def patch_contourf(wrapped, instance, args, kwargs):
    contours = wrapped(*args, **kwargs)
    for collection in contours.collections:
        collection.__is_contour_path = True

    return contours
