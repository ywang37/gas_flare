"""
Created on December 20, 2019

@author: Yi Wang
"""

import datetime
import sys

sys.path.append('/Dedicated/jwang-data/ywang/gas_flare/shared_code')
from gf_io import save_po
from popy import popy

#######################
# Start user parameters
#

in_dir = '/Dedicated/jwang-data/shared_satData/TROPOMI/NO2/US/2018/'
#in_dir = '/Dedicated/jwang-data/ywang/gas_flare/data/TROPOMI/NO2/'

out_dir = '/Dedicated/jwang-data/ywang/gas_flare/oversample/data/'

instrum = 'TROPOMI'

product = 'NO2'

grid_size= 0.01

# region
west  = -100.0
east  = -80.0
south = 17.0
north = 31.0

# start date
start_year  = 2018
start_month = 4
start_day   = 30

# end date
end_year  = 2019
end_month = 8
end_day   = 5

s5p_product = '*'

var = [ \
        {'varname': 'column_amount', 
            'longname': 'nitrogendioxide_tropospheric_column',
            'units': 'mol m-2'}, \
        ]

#
# End user parameters
#####################

out_file = instrum + '_' + product + '_' + str(grid_size) + '_' + \
        str(datetime.datetime(start_year, start_month, start_day))[0:10] + \
        '_' + str(datetime.datetime(end_year, end_month, end_day))[0:10] + \
        '.nc'

# initialization
print('Initializing ...')
po = popy(instrum, product,
        grid_size=grid_size,
        west=west, east=east, south=south, north=north,
        start_year=start_year, start_month=start_month, start_day=start_day,
        end_year=end_year, end_month=end_month, end_day=end_day,
        end_hour=23,end_minute=59,end_second=59,
        )

# load data
print('Loading data ...')
po.F_subset_S5PNO2(in_dir, s5p_product=s5p_product)

# oversample
print('Oversampling ...')
po.F_regrid()

# save data
print('Saving data ...')
filename = out_dir + out_file
save_po(po, filename, var)

#
print('Finished')





