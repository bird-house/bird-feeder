import logging
logger = logging.getLogger(__name__)


def feed_from_thredds(url, solr_url, depth=0):
    import pysolr
    import threddsclient
    logger.info("tds=%s, solr=%s", url, solr_url)
    solr = pysolr.Solr(solr_url, timeout=10)

    records = []
    for ds in threddsclient.crawl(url, depth=depth):
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



