"""
Created on December 23, 2019

@author: Yi Wang
"""

import matplotlib.pyplot as plt
import numpy as np

from mylib.cartopy_plot import cartopy_plot
from mylib.io import read_nc


#######################
# Start user parameters
#

#name = 'TROPOMI_NO2_0.01_2018-09-01_2018-09-30'
name = 'TROPOMI_NO2_0.01_2018-01-01_2018-12-31'

data_dir = '/Dedicated/jwang-data/ywang/gas_flare/oversample/data/'

fig_dir = '/Dedicated/jwang-data/ywang/gas_flare/oversample/figure/'

vmin = 0.0
vmax = 0.00006

cl_res = '50m'

xtick = np.arange(-180, 180.1, 5)
ytick = np.arange(-90, 90.1, 5)

region_limit = [17, -100, 31, -80]

#
# End user parameters
#####################

# read data
filename = data_dir + name + '.nc'
data = read_nc(filename, ['lat_e', 'lon_e', 'column_amount'])
lat_e = data['lat_e']
lon_e = data['lon_e']
lon_e, lat_e = np.meshgrid(lon_e, lat_e)
column_amount = data['column_amount']

# plot
cbar_prop = {}
cbar_prop['orientation'] = 'horizontal'
cartopy_plot(lon_e, lat_e, column_amount, vmin=vmin, vmax=vmax,
        cbar_prop=cbar_prop, cl_res=cl_res, region_limit=region_limit,
        xtick=xtick, ytick=ytick)


# save figure
figname = fig_dir + name + '.png'
plt.savefig(figname, format='png', dpi=300)
