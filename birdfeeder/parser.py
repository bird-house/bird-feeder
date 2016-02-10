import os
from netCDF4 import Dataset
import threddsclient
from birdfeeder import spider
from birdfeeder import walker
from dateutil import parser as dateparser

import logging
logger = logging.getLogger(__name__)


class Parser(object):
    """
    code is based on https://github.com/EarthSystemCoG/esgfpy-publish
    """
    
    def crawl(self):
        raise NotImplemented


class ThreddsParser(Parser):
    def __init__(self, url, depth=0):
        Parser.__init__(self)
        self.url = url
        self.depth = depth
        self.cat = threddsclient.read_url(url)

    def parse(self, ds):
        metadata = dict(
            source=self.cat.url,
            title=ds.name,
            category='thredds',
            subject=self.cat.name,
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

            
class SpiderParser(Parser):
    def __init__(self, url, depth=0):
        Parser.__init__(self)
        self.url = url
        self.depth = depth

    def parse(self, ds):
        metadata = dict(
            source=self.url,
            title=ds.name,
            category='spider',
            content_type=ds.content_type,
            last_modified=ds.last_modified,
            resourcename=ds.path,
            url=ds.download_url,
            size=ds.size,
            )
        return metadata
    
    def crawl(self):
        for ds in spider.crawl(self.url, depth=self.depth):
            yield self.parse(ds)
            

class WalkerParser(Parser):
        
    def __init__(self, start_dir):
        Parser.__init__(self)
        self.start_dir = start_dir

            
    def parse(self, dataset):
        metadata = dict(
            source = self.start_dir,
            title = dataset.name,
            category = "files",
            url = dataset.url,
            content_type = dataset.content_type,
            resourcename = dataset.path,
            variable = dataset.variable,
            variable_long_name = dataset.variable_long_name,
            cf_standard_name = dataset.cf_standard_name,
            units = dataset.units,
            comment = dataset.comments,
            institute = dataset.institute,
            experiment = dataset.experiment,
            project = dataset.project,
            model = dataset.model,
            frequency = dataset.frequency,
            creation_date = dataset.creation_date,
            last_modified=dataset.last_modified,
            size=dataset.size,
            )
        return metadata

    def crawl(self):
        for ds in walker.crawl(self.start_dir):
            yield self.parse(ds)
        





