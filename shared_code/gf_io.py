"""
Created on December 20, 2019

@author: Yi Wang
"""

from netCDF4 import Dataset

def save_nighttime_light(filename, lat_c, lon_c, radiance, count,
        verbose=True):
    """ Save nighttime light.
    """

    if verbose:
        print(' - save_nighttime_light: output ' + filename)

    # open file
    nc_f = Dataset(filename, 'w')

    # Dimensions of a netCDF file
    dim_lat_c = nc_f.createDimension('lat_c', len(lat_c))
    dim_lon_c = nc_f.createDimension('lon_c', len(lon_c))

    # Create variables in a netCDF file
    lat_c_v = nc_f.createVariable('lat_c', 'f4', ('lat_c',))
    lon_c_v = nc_f.createVariable('lon_c', 'f4', ('lon_c',))
    radiance_v = nc_f.createVariable('radiance', 'f4', ('lat_c','lon_c'))
    count_v = nc_f.createVariable('count', 'f4', ('lat_c','lon_c'))

    # Add attributes to variables
    radiance_v.units = 'nW/cm^2/sr'

    # Write variables
    lat_c_v[:] = lat_c
    lon_c_v[:] = lon_c
    radiance_v[:,:] = radiance
    count_v[:,:] = count

    # close file
    nc_f.close()

def save_po(po, filename, var, verbose=True):
    """ Save popy results.

    Parameters
    ----------
    po : popy instance
    filename : str
        save data to filename
    var: list
        Elements are dict.
        {varname: varname, longname: longname, units: units}

    """

    if verbose:
        print(' - save_po: output ' + filename)

    # open file
    nc_f = Dataset(filename, 'w')

    # latitude and longitude
    xgrid = po.xgrid
    ygrid = po.ygrid
    xgridr = po.xgridr
    ygridr = po.ygridr

    # Dimensions of a netCDF file
    dim_lat_c = nc_f.createDimension('lat_c', len(ygrid))
    dim_lon_c = nc_f.createDimension('lon_c', len(xgrid))
    dim_lat_e = nc_f.createDimension('lat_e', len(ygridr))
    dim_lon_e = nc_f.createDimension('lon_e', len(xgridr))

    # Create variables in a netCDF file
    lat_c_v = nc_f.createVariable('lat_c', 'f4', ('lat_c',))
    lon_c_v = nc_f.createVariable('lon_c', 'f4', ('lon_c',))
    lat_e_v = nc_f.createVariable('lat_e', 'f4', ('lat_e',))
    lon_e_v = nc_f.createVariable('lon_e', 'f4', ('lon_e',))
    nc_var_dict = {}
    for var_dict in var:
        varname = var_dict['varname']
        nc_var = nc_f.createVariable(varname, 'f4', ('lat_c', 'lon_c'))
        nc_var_dict[varname] = nc_var

    # Add attributes to variables
    for varname in nc_var_dict:
        nc_var = nc_var_dict[varname]
        for var_dict in var:
            if (var_dict['varname'] == varname):
                longname = var_dict.get('longname', None)
                if longname is not None:
                    nc_var.longname = longname
                units = var_dict.get('units', None)
                if units is not None:
                    nc_var.units = units

    # Write variables
    lat_c_v[:] = ygrid
    lon_c_v[:] = xgrid
    lat_e_v[:] = ygridr
    lon_e_v[:] = xgridr
    for varname in nc_var_dict:
        nc_var = nc_var_dict[varname]
        nc_var[:,:] = po.C[varname]

    # close file
    nc_f.close()
