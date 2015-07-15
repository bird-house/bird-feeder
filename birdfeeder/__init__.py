import sys

from .client import feed_from_thredds

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)


def create_parser():
    import argparse

    parser = argparse.ArgumentParser(
        prog="birdfeeder",
        usage='''birdfeeder [<options>] <command> [<args>]''',
        description="Feed Solr with Metadata and access URLs from NetCDF files",
        )
    parser.add_argument("--debug",
                        help="enable debug mode",
                        action="store_true")
    parser.add_argument("--service",
                        dest='service',
                        required=False,
                        type=type(''),
                        default='http://localhost:8983/solr/birdhouse',
                        help="Solr URL. Default: http://localhost:8983/solr/birdhouse",
                        action="store")
    subparsers = parser.add_subparsers(
            dest='command',
            title='command',
            description='List of available commands',
            help='Run "birdfeeder <command> -h" to get additional help.'
            )

    subparser = subparsers.add_parser(
        'from-thredds',
        prog="birdfeeder from-thredds",
        help="Publish datasets to solr."
        )

    subparser.add_argument("--catalog-url",
                        dest='catalog_url',
                        required=True,
                        type=type(''),
                        help="Thredds Catalog URL",
                        action="store")
    subparser.add_argument("--depth",
                        dest='depth',
                        required=False,
                        type=type(0),
                        help="Depth level for Thredds catalog crawler",
                        action="store")
   
    return parser


def execute(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)
    return feed_from_thredds(service=args.service, catalog_url=args.catalog_url, depth=args.depth)

def main():
    import argcomplete

    logger.setLevel(logging.INFO)

    parser = create_parser()
    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    execute(args)

if __name__ == '__main__':
    sys.exit(main())
