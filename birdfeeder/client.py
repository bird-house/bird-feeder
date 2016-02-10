import pysolr
import threddsclient
from timeit import default_timer as timer
from datetime import timedelta
import csv

from birdfeeder.parser import ThreddsParser, WalkerParser, SpiderParser

import logging
logger = logging.getLogger(__name__)


def write_spider(url, depth=0, filename='out.csv'):
    logger.info('Starting spider %s, depth=%s ...', url, depth)
    write(parser=SpiderParser(url, depth=depth), filename=filename)

    
def write_walker(start_dir, filename='out.csv'):
    logger.info('Starting walker %s ...', start_dir)
    write(parser=WalkerParser(start_dir), filename=filename)

    
def clear(service):
    solr = pysolr.Solr(service, timeout=10)
    logger.info("deletes all datasets from solr %s", service)
    solr.delete(q='*:*')
   

def feed_from_thredds(service, catalog_url, depth=1, maxrecords=-1, batch_size=50000):    
    logger.info("solr=%s, thredds catalog=%s", service, catalog_url)
    publish(service, parser=ThreddsParser(catalog_url, depth), maxrecords=maxrecords, batch_size=batch_size)
    
    
def feed_from_walker(service, start_dir, maxrecords=-1, batch_size=50000):
    logger.info("solr=%s, start dir=%s", service, start_dir)
    publish(service, parser=WalkerParser(start_dir), maxrecords=maxrecords, batch_size=batch_size)


def feed_from_spider(service, url, depth=1, maxrecords=-1, batch_size=50000):    
    logger.info("solr=%s, file service=%s", service, url)
    publish(service, parser=SpiderParser(url, depth), maxrecords=maxrecords, batch_size=batch_size)

    
def publish(service, parser, maxrecords=-1, batch_size=50000):    
    solr = pysolr.Solr(service, timeout=10)

    records = []
    for metadata in parser.crawl():
        # TODO: size is currently not part of schema
        if 'size' in metadata: del metadata['size']
        records.append(metadata)
        if len(records) >= batch_size:
            # publish if batch size is reached
            logger.info("publish %d records", len(records))
            solr.add(records)
            records = [] # reset records
        elif maxrecords >=0 and len(records) >= maxrecords:
            # stop publishing if max records reached
            break
    logger.info("publish %d records", len(records))
    solr.add(records)

def write(parser, filename='out.csv', batch_size=1000):
    start = timer()
    with open(filename, 'w') as csvfile:
        fieldnames = ['path', 'name', 'last_modified', 'size']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        
        ds_counter = 0
        records = []
        for ds in parser.crawl():
            records.append({'path': ds['resourcename'],
                             'name': ds['title'],
                             'last_modified': ds['last_modified'],
                             'size': ds['size']})
            if len(records) > batch_size:
                writer.writerows(records)
                end = timer()
                elapsed_time = timedelta(seconds=int(end-start))
                logger.info('{0} datasets written, elapsed time = {1} ...'.format(ds_counter, elapsed_time))
                records = [] # reset records
            ds_counter += 1
        # write last records
        if len(records) > 0:
            writer.writerows(records)
    end = timer()
    elapsed_time = timedelta(seconds=int(end-start))
    logger.info('{0} datasets written to {1}. Total elapsed time = {2}.'.format(ds_counter, filename, elapsed_time))


