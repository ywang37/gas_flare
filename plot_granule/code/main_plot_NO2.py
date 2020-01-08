"""
Created on November 6, 2019

@author: Yi Wang
"""

import glob
import matplotlib.pyplot as plt
import numpy as np

from mylib.pro_tropomi.plot_tropomi import plot_granule_tropomi_no2

#######################
# Start user parameters
#

data_root_dir = '/Dedicated/jwang-data/ywang/gas_flare/data/TROPOMI/NO2/'

fig_root_dir = '/Dedicated/jwang-data/ywang/gas_flare/plot_granule/figure/'

# parameter directory
para_dict = {
        '20180917T182618_20180917T193059' : {},
        }

#
# End user parameters
#####################


file_root_list = list(para_dict)
file_root_list.sort()

for i in range(len(file_root_list)):
    
    wildcard = data_root_dir + 'S5P_RPRO_L2__NO2____' \
            + file_root_list[i] + '*.nc'
    filename = glob.glob(wildcard)
    if len(filename) == 1:
        filename = filename[0]
    
    args = (
            'PRODUCT/longitude', 
            'PRODUCT/latitude',
            'PRODUCT/nitrogendioxide_tropospheric_column',
            filename
            )
    region_limit = [12, -100, 31, -80]
    plot_granule_tropomi_no2(*args, region_limit=region_limit,
            xtick=np.arange(-180,180.1,5),
            ytick=np.arange(-90,90.1,2), cl_res='10m',
            vmax=0.00006, vmin=0)
    plt.savefig('test.png', format='png', dpi=300)
