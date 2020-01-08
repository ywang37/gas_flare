"""
Created on January 7, 2020

@author: Yi Wang
"""

#import matplotlib.pyplot as plt
import numpy as np
import sys

from mylib.grid_utility import generate_grid_2
from mylib.regrid import drop_in_the_box

sys.path.append('/Dedicated/jwang-data/ywang/gas_flare/shared_code')
from gf_io import save_nighttime_light
import gf_para

#######################
# Start user parameters
#

infile_name_list = ['201808']

root_data_dir = '/Dedicated/jwang-data/ywang/gas_flare/\
regrid_nighttime_light/data/Gulf_of_Mexico/'

out_filname = None

region_name = 'gulf_of_mexico'

# resolution
lat_step = 0.01
lon_step = 0.01

#
# End user parameters
#####################

# region
lat_start = gf_para.region_dict[region_name][0]
lat_end   = gf_para.region_dict[region_name][2]
lon_start = gf_para.region_dict[region_name][1]
lon_end   = gf_para.region_dict[region_name][3]

# generate latitude and longitude
lat_e, lon_e, lat_c, lon_c = \
        generate_grid_2(lat_step, lat_start, lat_end,
                lon_step, lon_start, lon_end)


# output region
print(region_name)
print('lat_start = {}'.format(lat_start))
print('lat_end = {}'.format(lat_end))
print('lon_start = {}'.format(lon_start))
print('lon_end = {}'.format(lon_end))
print('lat_step = {}'.format(lat_step))
print('lon_step = {}'.format(lon_step))
print('latitude edge: ')
print(lat_e)
print('latitude center: ')
print(lat_c)
print('longitude edge: ')
print(lon_e)
print('longitude center: ')
print(lon_c)

# read data
radiance_list = []
rad_mask_list = []
lat_list = []
lon_list = []
ori_data_dir = root_data_dir + 'original/'
for i in range(len(infile_name_list)):

    infile_name = infile_name_list[i]
    
    # radiance
    radiance_file = ori_data_dir + infile_name + '.radiance.npy'
    radiance = np.load(radiance_file)
    radiance_list.append(radiance)

    # radiance mask
    rad_mask_file = ori_data_dir + infile_name + '.radMask.npy'
    rad_mask = np.load(rad_mask_file)
    rad_mask_list.append(rad_mask)

    # latitude
    lat_file = ori_data_dir + 'lat.npy'
    lat = np.load(lat_file)
    lat_list.append(lat)

    # longitude
    lon_file = ori_data_dir + 'lon.npy'
    lon = np.load(lon_file)
    lon_list.append(lon)

# regrid
data = drop_in_the_box(radiance_list, lat_list, lon_list,
        lat_start, lat_end, lat_step,
        lon_start, lon_end, lon_step,
        weight_list=rad_mask_list)

# save data
regrid_data_dir = root_data_dir + 'regrid/'
if len(infile_name_list) == 1:
    out_file = regrid_data_dir + infile_name_list[0] + '.nc'
else:
    if out_filname is None:
        out_file = regrid_data_dir + \
                infile_name_list[0] + '_' + infile_name_list[-1] + '.nc'
    else:
        out_file = regrid_data_dir + out_filname

save_nighttime_light(out_file, lat_c, lon_c, 
        data['value'], data['count'])
