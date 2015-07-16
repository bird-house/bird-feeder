import os
from netCDF4 import Dataset

import logging
logger = logging.getLogger(__name__)


def add_metadata(metadata, key, value):
    if not key in metadata:
        metadata[key] = [] 
    metadata[key].append(value)

def parse_netcdf(filepath):
    logger.debug("parse %s", filepath)
    metadata = {}
    metadata['name'] = os.path.basename(filepath)
    metadata['url'] = 'file://' + filepath
    
    try:
        ds = Dataset(filepath, 'r')

        # loop over global attributes
        for attname in ds.ncattrs():
            attvalue = getattr(ds, attname)
            add_metadata(metadata, attname, attvalue)

        # loop over dimensions
        for key, dim in ds.dimensions.items():
            add_metadata(metadata, 'dimension', "%s:%s" % (key, len(dim)) )

        # loop over variable attributes
        for key, variable in ds.variables.items():
            if key in ds.dimensions:
                # skip dimension variables
                continue
            if '_bnds' in key:
                continue
            if key in ['lat', 'lon', 'height', 'rotated_pole']:
                continue
            add_metadata(metadata, 'variable', key)
            add_metadata(metadata, 'variable_long_name', getattr(variable, 'long_name', None) )
            cf_standard_name = getattr(variable, 'standard_name', None)
            if cf_standard_name is not None:
                add_metadata(metadata, 'cf_standard_name', getattr(variable, 'standard_name', None) )
            add_metadata(metadata, 'units', getattr(variable, 'units', None) )

    except Exception as e:
        logging.error(e)
    finally:
        try:
            ds.close()
        except:
            pass
    
    return metadata
