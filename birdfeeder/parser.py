import os
from netCDF4 import Dataset
import threddsclient

import logging
logger = logging.getLogger(__name__)

class Parser(object):
    """
    code is based on https://github.com/EarthSystemCoG/esgfpy-publish
    """
    def add_metadata(self, metadata, key, value):
        if not key in metadata:
            metadata[key] = [] 
        metadata[key].append(value)
    
    def crawl(self):
        raise NotImplemented


class ThreddsParser(Parser):
    def __init__(self, url, depth):
        Parser.__init__(self)
        self.url = url
        self.depth = depth

    def parse(self, ds):
        metadata = dict(
            title=ds.name,
            content_type=ds.content_type,
            last_modified=ds.modified,
            resourcename=ds.ID,
            url=ds.download_url(),
            opendap_url=ds.opendap_url(),
            wms_url=ds.wms_url(),
            catalog_url=ds.url)
        return metadata
    
    def crawl(self):
        for ds in threddsclient.crawl(self.url, depth=self.depth):
            yield self.parse(ds)


class NetCDFParser(Parser):
    def __init__(self, start_dir):
        Parser.__init__(self)
        self.start_dir = start_dir

    def parse(self, filepath):
        logger.debug("parse %s", filepath)
        metadata = {}
        metadata['name'] = os.path.basename(filepath)
        metadata['url'] = 'file://' + filepath

        try:
            ds = Dataset(filepath, 'r')

            # loop over global attributes
            for attname in ds.ncattrs():
                attvalue = getattr(ds, attname)
                self.add_metadata(metadata, attname, attvalue)

            # loop over dimensions
            for key, dim in ds.dimensions.items():
                self.add_metadata(metadata, 'dimension', "%s:%s" % (key, len(dim)) )

            # loop over variable attributes
            for key, variable in ds.variables.items():
                if key in ds.dimensions:
                    # skip dimension variables
                    continue
                if '_bnds' in key:
                    continue
                if key in ['lat', 'lon', 'height', 'rotated_pole']:
                    continue
                self.add_metadata(metadata, 'variable', key)
                self.add_metadata(metadata, 'variable_long_name', getattr(variable, 'long_name', None) )
                cf_standard_name = getattr(variable, 'standard_name', None)
                if cf_standard_name is not None:
                    self.add_metadata(metadata, 'cf_standard_name', getattr(variable, 'standard_name', None) )
                self.add_metadata(metadata, 'units', getattr(variable, 'units', None) )

        except Exception as e:
            logging.error(e)
        finally:
            try:
                ds.close()
            except:
                pass

        return metadata

    def map_fields(self, metadata):
        record = dict(
            title = metadata.get('name'),
            url = metadata.get('url'),
            variable = metadata.get('variable'),
            variable_long_name = metadata.get('variable_long_name'),
            cf_standard_name = metadata.get('cf_standard_name'),
            units = metadata.get('units'),
            comment = metadata.get('comments'),
            institution = metadata.get('institution'),
            institute_id = metadata.get('institute_id'),
            experiment = metadata.get('experiment'),
            project_id = metadata.get('project_id'),
            model_id = metadata.get('model_id'),
            )
        return record

    def crawl(self):
        if not os.path.isdir(self.start_dir):
            raise Exception("Invalid start directory: %s", self.start_dir)
        
        logger.info('start directory = %s', self.start_dir)

        for directory, subdirs, files in os.walk(self.start_dir):
            # loop over files in this directory
            for filename in files:
                # ignore hidden files and thumbnails
                if not filename[0] == '.' and not 'thumbnail' in filename and not filename.endswith('.xml'):
                    filepath = os.path.join(directory, filename)
                    yield self.map_fields(self.parse(filepath))
        





