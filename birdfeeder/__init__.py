import sys

from birdfeeder.client import run_spider, clear, feed_from_thredds, feed_from_directory, feed_from_spider

import logging
logging.basicConfig(format='%(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)


def create_parser():
    import argparse

    parser = argparse.ArgumentParser(
        prog="birdfeeder",
        usage='''birdfeeder [<options>] <command> [<args>]''',
        description="Feeds Solr with Datasets (NetCDF Format) from Thredds Catalogs and File System.",
        )
    parser.add_argument("-v",
                        dest="verbose",
                        help="enable verbose mode",
                        action="store_true")
    parser.add_argument("--service",
                        dest='service',
                        required=False,
                        type=type(''),
                        default='http://localhost:8983/solr/birdhouse',
                        help="Solr URL. Default: http://localhost:8983/solr/birdhouse",
                        action="store")
    parser.add_argument("--maxrecords",
                        dest='maxrecords',
                        required=False,
                        type=type(-1),
                        default=-1,
                        help="Maximum number of records to publish. Default: -1 (unlimited)",
                        action="store")
    parser.add_argument("--batch-size",
                        dest='batch_size',
                        required=False,
                        type=type(1),
                        default=50000,
                        help="Batch size of records to publish. Default: 50000",
                        action="store")
    subparsers = parser.add_subparsers(
            dest='command',
            title='command',
            description='List of available commands',
            help='Run "birdfeeder <command> -h" to get additional help.'
            )

    # spider command
    subparser = subparsers.add_parser(
        'spider',
        prog="birdfeeder spider",
        help="Runs spider to crawl NetCDF files on a HTTP file service and writes the URL list to a CSV file."
        )

    subparser.add_argument("--url",
                        dest='url',
                        required=True,
                        type=type(''),
                        help="HTTP file service URL",
                        action="store")
    subparser.add_argument("--depth",
                        dest='depth',
                        required=False,
                        type=type(0),
                        default=100,
                        help="Depth level for crawler. Default: 100",
                        action="store")
    subparser.add_argument("-o",
                        dest='output',
                        required=False,
                        type=type(''),
                        default='out.csv',
                        help="Filename of the output CSV file. Default: out.csv",
                        action="store")
     
    # clear command
    subparser = subparsers.add_parser(
        'clear',
        prog="birdfeeder clear",
        help="Clears the complete solr index. Use with caution!"
        )
     
    # from-thredds command
    subparser = subparsers.add_parser(
        'from-thredds',
        prog="birdfeeder from-thredds",
        help="Publish datasets from Thredds Catalog to Solr."
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

    # from-directory command
    subparser = subparsers.add_parser(
        'from-directory',
        prog="birdfeeder from-directory",
        help="Publish NetCDF files from directory to Solr."
        )

    subparser.add_argument("--start-dir",
                        dest='start_dir',
                        required=True,
                        type=type(''),
                        help="Start directory",
                        action="store")

    # from-spider command
    subparser = subparsers.add_parser(
        'from-spider',
        prog="birdfeeder from-spider",
        help="Runs spider to crawl NetCDF files on a HTTP file service and publishes them to Solr."
        )

    subparser.add_argument("--url",
                        dest='url',
                        required=True,
                        type=type(''),
                        help="HTTP file service URL",
                        action="store")
    subparser.add_argument("--depth",
                        dest='depth',
                        required=False,
                        type=type(0),
                        default=100,
                        help="Depth level for crawler. Default: 100",
                        action="store")
   
    return parser


def execute(args):
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    if args.command == 'spider':
        run_spider(url=args.url, depth=args.depth, filename=args.output)
    elif args.command == 'clear':
        clear(service=args.service)
    elif args.command == 'from-thredds':
        feed_from_thredds(service=args.service, catalog_url=args.catalog_url, depth=args.depth,
                          maxrecords=args.maxrecords, batch_size=args.batch_size)
    elif args.command == 'from-directory':
        feed_from_directory(service=args.service, start_dir=args.start_dir,
                            maxrecords=args.maxrecords,
                            batch_size=args.batch_size)
    elif args.command == 'from-spider':
        feed_from_spider(service=args.service, url=args.url, depth=args.depth,
                            maxrecords=args.maxrecords,
                            batch_size=args.batch_size)
    logger.info('Done.')

def main():
    import argcomplete

    logger.setLevel(logging.INFO)

    parser = create_parser()
    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    execute(args)

if __name__ == '__main__':
    sys.exit(main())
