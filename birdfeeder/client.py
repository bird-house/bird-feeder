import logging
logger = logging.getLogger(__name__)


def feed(url, solr_url):
    import pysolr
    from threddsclient import client as tdsclient
    logger.info("tds=%s, solr=%s", url, solr_url)
    solr = pysolr.Solr(solr_url, timeout=10)
    ## results = solr.search('bananas')
    ## for result in results:
    ##     print "The title is '{0}'.".format(result['title'])

    for ds in tdsclient.crawl(url, depth=1):
        logger.info(ds.name)
        solr.add([ dict(id=ds.ID, title=ds.name) ])



