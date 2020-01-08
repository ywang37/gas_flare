"""
Created on December 23, 2019

@author: Yi Wang
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

from mylib.cartopy_plot import cartopy_plot, plot_rectangle
from mylib.constants import mol_m2_to_molec_cm2
from mylib.io import read_nc


sys.path.append('/Dedicated/jwang-data/ywang/gas_flare/shared_code')
import gf_para
from gf_plot import plot_two_variables

#######################
# Start user parameters
#

# NO2
#name = 'TROPOMI_NO2_0.01_2018-09-01_2018-09-30'
no2_name = 'TROPOMI_NO2_0.01_2018-05-01_2018-12-31'

no2_data_dir = '/Dedicated/jwang-data/ywang/gas_flare/oversample/data/'

no2_vmin = 0
no2_vmax = 2e15

no2_unit = r'NO$_2$ column density [molec cm$^{-2}$]'

cl_res = '50m'

# radiance
rad_name = '201808'

rad_data_dir = '/Dedicated/jwang-data/ywang/gas_flare/regrid_nighttime_light/\
data/Gulf_of_Mexico/regrid/'

rad_vmin = 0.0
rad_vmax = 30.0

rad_unit = r'Nighttime radiance [nW cm$^{-2}$ sr$^{-1}$]'

# other
xtick = np.arange(-180, 180.1, 0.2)
ytick = np.arange(-90, 90.1, 0.1)

lw = 0.5

figsize = (8, 6)

y_offset = -0.16

region_name = 'region1'
region_limit = gf_para.region_dict[region_name]

fig_dir = '../figure/'

sub_region_list = [
        gf_para.region_dict['region2'],
        gf_para.region_dict['region3']
        ]

no2_rad_sub_region_color = ('black', 'red')

#
# End user parameters
#####################

no2_title = '_'.join(no2_name.split('_')[-2:])
rad_title = rad_name


# read TROPOMI data
no2_filename = no2_data_dir + no2_name + '.nc'
no2_data = read_nc(no2_filename, ['lat_e', 'lon_e', 'column_amount'])
no2_lat_e = no2_data['lat_e']
no2_lon_e = no2_data['lon_e']
no2_lon_e, no2_lat_e = np.meshgrid(no2_lon_e, no2_lat_e)
no2_column_amount = no2_data['column_amount'] * mol_m2_to_molec_cm2

# read VIIRS nighttime light
rad_filename = rad_data_dir + rad_name + '.nc'
rad_data = read_nc(rad_filename, ['lat_c', 'lon_c', 'radiance', 'count'])
rad_value = rad_data['radiance']

# plot
pout = plot_two_variables(no2_lat_e, no2_lon_e, no2_column_amount, 
        no2_lat_e, no2_lon_e, rad_value,
        region_limit=region_limit, cl_res=cl_res,
        cl_color2='rosybrown',
        figsize=figsize,
        xtick=xtick, ytick=ytick,
        lw1=lw, lw2=lw,
        y_offset=y_offset,
        title1=no2_title, title2=rad_title,
        vmin1=no2_vmin, vmax1=no2_vmax,
        vmin2=rad_vmin, vmax2=rad_vmax,
        unit1=no2_unit, unit2=rad_unit,
        cmap2=plt.get_cmap('gray'))

for i in range(len(pout['pout'])):

    ax = pout['pout'][i]['ax']

    for j in range(len(sub_region_list)):

        sub_region = sub_region_list[j]

        color = no2_rad_sub_region_color[i]
        plot_rectangle(ax, sub_region, c=color)


# save figure
figname = fig_dir + region_name + '_' + no2_name \
        + '_radiance_' + rad_name + '.png'
plt.savefig(figname, format='png', dpi=300)
