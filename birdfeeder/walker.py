import os
from netCDF4 import Dataset as NCDataset
from dateutil import parser as dateparser

import logging
logger = logging.getLogger(__name__)

SPATIAL_VARIABLES =  [
    'longitude', 'lon',
    'latitude', 'lat',
    'altitude', 'alt', 'level', 'height',
    'rotated_pole',
    'rotated_latitude_longitude',
    'time']


class Dataset(object):
    def __init__(self, filepath):
        self.path = filepath
        self.name = os.path.basename(filepath)
        self.url = 'file://' + filepath
        self.content_type = 'application/netcdf'
        self.resourcename = filepath
        self.attributes = {}
        self._parse(filepath)

    def __str__(self):
        return "attributes={0}".format(self.attributes)

    @property
    def variable(self):
        return self.attributes.get('variable')

    @property
    def variable_long_name(self):
        return self.attributes.get('variable_long_name')

    @property
    def cf_standard_name(self):
        return self.attributes.get('cf_standard_name')

    @property
    def units(self):
        return self.attibutes.get('units')

    @property
    def comments(self):
        return self.attributes.get('comments')

    @property
    def institute(self):
        return self.attributes.get('institute_id')

    @property
    def experiment(self):
        return self.attributes.get('experiment_id')

    @property
    def project(self):
        return self.attibutes.get('project_id')

    @property
    def model(self):
        return self.attributes.get('model_id')
    
    @property
    def frequency(self):
        return self.attributes.get('frequency')

    @property
    def creation_date(self):
        if 'creation_date' in self.attributes:
            return self.attributes['creation_date'][0]
        else:
            return None

    @property
    def size(self):
        if 'size' in self.attributes:
            return self.attributes['size'][0]
        else:
            return ''

    @property
    def last_modified(self):
        return self.creation_date
        
    def _add_attribute(self, key, value):
        if not key in self.attributes:
            self.attributes[key] = [] 
        self.attributes[key].append(value)

    def _parse(self, filepath):
        filepath = os.path.abspath(filepath)
        logger.debug("parse %s", filepath)

        try:
            ds = NCDataset(filepath, 'r')

            # loop over global attributes
            for attname in ds.ncattrs():
                attvalue = getattr(ds, attname)
                if 'date' in attname.lower():
                    # must format dates in Solr format, if possible
                    try:
                        solr_dt = dateparser.parse(attvalue)
                        self._add_attribute(attname, solr_dt.strftime('%Y-%m-%dT%H:%M:%SZ') )
                    except:
                        pass # disregard this attribute
                else:
                    self._add_attribute(attname, attvalue)

            # loop over dimensions
            for key, dim in ds.dimensions.items():
                self._add_attribute('dimension', "%s:%s" % (key, len(dim)) )

            # loop over variable attributes
            for key, variable in ds.variables.items():
                if key.lower() in ds.dimensions:
                    # skip dimension variables
                    continue
                if '_bnds' in key.lower():
                    continue
                if key.lower() in SPATIAL_VARIABLES:
                    continue
                self._add_attribute('variable', key)
                self._add_attribute('variable_long_name', getattr(variable, 'long_name', None) )
                cf_standard_name = getattr(variable, 'standard_name', None)
                if cf_standard_name is not None:
                    self._add_attribute('cf_standard_name', getattr(variable, 'standard_name', None) )
                self._add_attribute('units', getattr(variable, 'units', None) )

        except Exception as e:
            logging.error(e)
        finally:
            try:
                ds.close()
            except:
                pass

 
def crawl(start_dir):
    if not os.path.isdir(start_dir):
        raise Exception("Invalid start directory: %s", start_dir)

    logger.info('start directory = %s', start_dir)

    for directory, subdirs, files in os.walk(start_dir):
        # loop over files in this directory
        for filename in files:
            # ignore hidden files and thumbnails
            if not filename[0] == '.' and not 'thumbnail' in filename and not filename.endswith('.xml'):
                filepath = os.path.join(directory, filename)
                yield Dataset(filepath)


        
            


   

    
        


