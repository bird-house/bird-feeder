import nose
from nose.tools import ok_
from nose.plugins.attrib import attr

from birdfeeder.parser import ThreddsParser, WalkerParser, SpiderParser

@attr('online')
def test_thredds_parser():
    parser = ThreddsParser(url="http://www.esrl.noaa.gov/psd/thredds/catalog.xml", depth=1)

def test_walker_parser():
    parser = WalkerParser(start_dir='.')
    
#@attr('online')
def test_spider_parser():
    parser = SpiderParser(
        url="http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/",
        depth=1)
