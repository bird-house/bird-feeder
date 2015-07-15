import os

import logging
logger = logging.getLogger(__name__)


class Dataset(object):
    def __init__(self, filepath):
        self.name = os.path.basename(filepath)
        self.url = "file://" + filepath

def parse_netcdf(filepath):
    logger.debug("parse %s", filepath)
    return Dataset(filepath)
