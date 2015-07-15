import logging
logger = logging.getLogger(__name__)


def clear(service):
    pass


def feed_from_thredds(service, catalog_url, depth=0):
    import pysolr
    import threddsclient
    logger.info("solr=%s, thredds catalog=%s", service, catalog_url)
    solr = pysolr.Solr(service, timeout=10)

    records = []
    for ds in threddsclient.crawl(catalog_url, depth=depth):
        logger.debug("add record %s", ds.name)
        record = dict(
            id=ds.ID,
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



