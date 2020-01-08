"""
Created on January 6, 2020

@author: Yi Wang
"""

import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np

from mylib.cartopy_plot import add_geoaxes
from mylib.cartopy_plot import cartopy_plot

def plot_two_variables(lat1, lon1, var1, lat2, lon2, var2,
        figsize=None, region_limit=None, cl_res=None,
        xtick = np.arange(-180, 180.1, 5),
        ytick = np.arange(-90, 90.1, 5),
        xtick1=None, ytick1=None, xtick2=None, ytick2=None,
        title1=None, title2=None,
        vmin1=None, vmax1=None, vmin2=None, vmax2=None,
        cl_color2='black',
        lw1=1, lw2=1,
        unit1='', unit2='',
        y_offset=-0.08,
        cmap1=None, cmap2=None):
    """ Plot two variables

    Parameters
    ----------

    """

    out_data = {}
    out_data['pout'] = []

    # figure and ax_list
    if figsize is None:
        figsize = (10, 5)
    fig = plt.figure(figsize=figsize)
    ax_list = []

    # ticks
    if xtick1 is None:
        xtick1 = xtick
    if ytick1 is None:
        ytick1 = ytick
    if xtick2 is None:
        xtick2 = xtick
    if ytick2 is None:
        ytick2 = []

    # colorbar paramters
    h = 0.03

    # plot var1
    ax1 = add_geoaxes(fig, 121, title=title1, xtick=xtick1, ytick=ytick1,
            cl_res=cl_res, lw=lw1)
    pout1 = cartopy_plot(lon1, lat1, var1, ax=ax1,
            vmin=vmin1, vmax=vmax1,
            cbar=False, cmap=cmap1)
    ax1.reset_position()
    ax_list.append(ax1)
    out_data['pout'].append(pout1)
    pos1 = pout1['ax'].get_position()
    cax1 = fig.add_axes([pos1.x0, pos1.y0+y_offset, pos1.width, h])
    cb1 = plt.colorbar(pout1['mesh'], cax=cax1,
            orientation='horizontal', extend='max')
    cb1.set_label(unit1)


    # plot var2 
    ax2 = add_geoaxes(fig, 122, title=title2, xtick=xtick2, ytick=ytick2,
            cl_res=cl_res, lw=lw2, cl_color=cl_color2)
    ax_list.append(ax2)
    pout2 = cartopy_plot(lon2, lat2, var2, ax=ax2,
            vmin=vmin2, vmax=vmax2,
            cbar=False, cmap=cmap2)
    out_data['pout'].append(pout2)
    pos2 = pout2['ax'].get_position()
    cax2 = fig.add_axes([pos2.x0, pos2.y0+y_offset, pos2.width, h])
    cb2 = plt.colorbar(pout2['mesh'], cax=cax2,
            orientation='horizontal', extend='max')
    cb2.set_label(unit2)

    # set region limit
    if region_limit is not None:
        for i in range(len(ax_list)):
            ax = ax_list[i]
            ax.set_xlim(region_limit[1], region_limit[3])
            ax.set_ylim(region_limit[0], region_limit[2])

    return out_data
