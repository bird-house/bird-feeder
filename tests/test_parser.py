import nose
from nose.tools import ok_
from nose.plugins.attrib import attr

from birdfeeder.parser import ThreddsParser, WalkerParser, SpiderParser

@attr('online')
def test_thredds_parser():
    parser = ThreddsParser(url="http://www.esrl.noaa.gov/psd/thredds/catalog/Datasets/ncep.reanalysis2/surface/catalog.xml", depth=1)
    datasets = [ds for ds in parser.crawl()]
    print datasets[0]
    assert datasets > 0
    assert datasets[0]['content_type'] == 'application/netcdf'
    assert datasets[0]['url'] == "http://www.esrl.noaa.gov/psd/thredds/fileServer/Datasets/ncep.reanalysis2/surface/hgt.sfc.nc"
    assert datasets[0]['last_modified'] == "2015-10-09T22:43:13Z"
    assert datasets[0]['title'] == "hgt.sfc.nc"

def test_walker_parser():
    parser = WalkerParser(start_dir='.')
    
#@attr('online')
def test_spider_parser():
    parser = SpiderParser(
        url="http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/",
        depth=1)
