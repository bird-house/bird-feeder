import sys

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARN)
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

def create_parser():
    import argparse

    parser = argparse.ArgumentParser(
        prog="birdfeeder",
        usage='''birdfeeder [<options>]''',
        description="Feed solr from thredds",
        )
    parser.add_argument("--catalog-url",
                        dest='catalog_url',
                        required=True,
                        type=type(''),
                        help="Thredds Catalog URL",
                        action="store")
    parser.add_argument("--solr-url",
                        dest='solr_url',
                        required=False,
                        type=type(''),
                        default='http://localhost:8983/solr/',
                        help="Solr URL",
                        action="store")
    return parser


def execute(args):
    return feed(args.catalog_url, args.solr_url)

def main():
    import argcomplete

    logger.setLevel(logging.INFO)

    parser = create_parser()
    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    execute(args)

if __name__ == '__main__':
    sys.exit(main())

