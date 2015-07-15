import os
from . parser import parse_netcdf

import logging
logger = logging.getLogger(__name__)

def crawl(start_dir, maxrecords=-1):
    """
    based on esgfpy-publish
    
    https://github.com/EarthSystemCoG/esgfpy-publish/blob/master/esgfpy/publish/services.py
    """
    
    if not os.path.isdir(start_dir):
        raise Exception("Invalid start directory: %s", start_dir)

    logger.info('start directory = %s', start_dir)

    records = []
    for directory, subdirs, files in os.walk(start_dir):
        # loop over files in this directory
        for file in files:
            if maxrecords < 0 or len(records) < maxrecords-1:
                # ignore hidden files and thumbnails
                if not file[0] == '.' and not 'thumbnail' in file and not file.endswith('.xml'):
                    filepath = os.path.join(directory, file)
                    record = parse_netcdf(filepath)
                    if record is not None:
                        records.append(record)

    return records
                        
    
