import pysolr
import threddsclient
from . crawler import crawl

import logging
logger = logging.getLogger(__name__)


def clear(service):
    solr = pysolr.Solr(service, timeout=10)
    logger.info("deletes all datasets from solr %s", service)
    solr.delete(q='*:*')
   

def feed_from_thredds(service, catalog_url, depth=0):    
    logger.info("solr=%s, thredds catalog=%s", service, catalog_url)
    solr = pysolr.Solr(service, timeout=10)

    records = []
    for ds in threddsclient.crawl(catalog_url, depth=depth):
        logger.debug("add record %s", ds.name)
        record = dict(
            title=ds.name,
            content_type=ds.content_type,
            last_modified=ds.modified,
            resourcename=ds.ID,
            url=ds.download_url(),
            opendap_url=ds.opendap_url(),
            wms_url=ds.wms_url(),
            catalog_url=ds.url)
        records.append(record)
    logger.info("publish %d records", len(records))
    solr.add(records)

    
def feed_from_directory(service, start_dir, maxrecords=-1):
    logger.info("solr=%s, start dir=%s", service, start_dir)
    solr = pysolr.Solr(service, timeout=10)

    records = []
    for ds in crawl(start_dir, maxrecords):
        logger.debug("add record %s", ds.name)
        record = dict(
            title=ds.name,)
        records.append(record)
    logger.info("publish %d records", len(records))
    #solr.add(records)
        


