import logging
logger = logging.getLogger(__name__)


def feed(url, solr_url):
    import pysolr
    import threddsclient
    logger.info("tds=%s, solr=%s", url, solr_url)
    solr = pysolr.Solr(solr_url, timeout=10)

    for ds in threddsclient.crawl(url, depth=1):
        logger.info(ds.name)
        solr.add([ dict(
            id=ds.ID,
            title=ds.name,
            content_type=ds.content_type,
            last_modified=ds.modified,
            resourcename=ds.ID,
            url=ds.download_url(),
            opendap_url=ds.opendap_url(),
            wms_url=ds.wms_url(),
            catalog_url=ds.url)])



