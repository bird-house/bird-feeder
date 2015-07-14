import sys

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)


def feed(thredds_url, solr_url):
    pass

def create_parser():
    import argparse

    parser = argparse.ArgumentParser(
        prog="birdfeeder",
        usage='''birdfeeder [<options>]''',
        description="Feed solr from thredds",
        )
    parser.add_argument("--thredds-url",
                        dest='thredds_url',
                        required=True,
                        help="Thredds Catalog URL",
                        action="store")
    parser.add_argument("--solr-url",
                        dest='solr_url',
                        required=True,
                        help="Solr URL",
                        action="store")
    return parser


def execute(args):
    return feed(args.thredds_url, args.solr_url)

def main():
    import argcomplete

    logger.setLevel(logging.INFO)

    parser = create_parser()
    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    execute(args)

if __name__ == '__main__':
    sys.exit(main())

