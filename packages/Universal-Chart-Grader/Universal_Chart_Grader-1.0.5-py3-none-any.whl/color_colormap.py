import matplotlib.colors as mcolors
import matplotlib.cm, matplotlib._cm_listed
import matplotlib.pyplot as plt

import mpl_converter

# Hex -> CSS Name
css_hex_to_name = {hex.lower(): name.lower() for name, hex in mcolors.CSS4_COLORS.items()}

# MPL Names -> CSS Names / Hex
color_name_to_css_name = {}
for name, color in mcolors._colors_full_map.items():
    hex = mcolors.to_hex(color).lower()
    if hex in css_hex_to_name:
        color_name_to_css_name[name.lower()] = css_hex_to_name[hex]

# Colormap
is_list_colormap_data = lambda data: isinstance(data, dict) and ('list' in data or 'listed' in data)
cmaps_gradient_data = {name: data for name, data in matplotlib.cm.datad.items()
                       if not is_list_colormap_data(data)}
cmaps_constant_data = {
    'magma'  : matplotlib._cm_listed._magma_data,
    'inferno': matplotlib._cm_listed._inferno_data,
    'plasma' : matplotlib._cm_listed._plasma_data,
    'viridis': matplotlib._cm_listed._viridis_data,
    'cividis': matplotlib._cm_listed._cividis_data,
    # 'twilight'        : matplotlib._cm_listed._twilight_data,
    # 'twilight_shifted': matplotlib._cm_listed._twilight_shifted_data,
    **{name: data for name, data in matplotlib.cm.datad.items()
       if is_list_colormap_data(data)}
}

mpl_cmap_data = {}
mpl_cmaps = {}
for name in plt.colormaps():
    if name.endswith('_r'): continue

    if name in cmaps_gradient_data:
        mpl_cmap_data[name.lower()] = cmaps_gradient_data[name]
        mpl_cmaps[name.lower()] = mpl_converter.mpl_linear_data_to_uhe(cmaps_gradient_data[name])
    elif name in cmaps_constant_data:
        cmap_data = cmaps_constant_data[name]
        if is_list_colormap_data(cmap_data):
            mpl_cmap_data[name.lower()] = cmap_data['listed']
            mpl_cmaps[name.lower()] = mpl_converter.mpl_listed_data_to_uhe(cmap_data['listed'])
        else:
            mpl_cmap_data[name.lower()] = cmap_data
            mpl_cmaps[name.lower()] = mpl_converter.mpl_listed_data_to_uhe(cmap_data)