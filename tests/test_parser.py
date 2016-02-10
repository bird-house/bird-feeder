import nose
from nose.tools import ok_
from nose.plugins.attrib import attr

from birdfeeder.parser import ThreddsParser, WalkerParser, SpiderParser

from tests.common import TESTDATA_PATH

@attr('online')
def test_thredds_parser():
    parser = ThreddsParser(url="http://www.esrl.noaa.gov/psd/thredds/catalog/Datasets/ncep.reanalysis2/surface/catalog.xml", depth=1)
    datasets = [ds for ds in parser.crawl()]
    
    assert datasets > 0

    print datasets[0]

    assert datasets[0]['content_type'] == 'application/netcdf'
    assert datasets[0]['url'] == "http://www.esrl.noaa.gov/psd/thredds/fileServer/Datasets/ncep.reanalysis2/surface/hgt.sfc.nc"
    assert datasets[0]['last_modified'] == "2015-10-09T22:43:13Z"
    assert datasets[0]['title'] == "hgt.sfc.nc"

def test_walker_parser():
    parser = WalkerParser(start_dir=TESTDATA_PATH)
    datasets = [ds for ds in parser.crawl()]
    assert len(datasets) == 1

    print datasets[0]
    
    assert datasets[0]['content_type'] == 'application/netcdf'
    assert 'tasmax' in datasets[0]['url']
    assert datasets[0]['last_modified'] == "2015-05-06T13:22:33Z"
    assert datasets[0]['title'] == "tasmax_EUR-44_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200602-200612.nc"
    assert datasets[0]['resourcename'] == "/CORDEX/EUR-44/mon/tasmax_EUR-44_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200602-200612.nc"
    assert datasets[0]['size'] == '301.2K'
    
@attr('online')
def test_spider_parser():
    parser = SpiderParser(
        url="http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/",
        depth=1)
    datasets = [ds for ds in parser.crawl()]
    
    assert datasets > 0

    print datasets[0]
    
    assert datasets[0]['content_type'] == 'application/netcdf'
    assert datasets[0]['url'] == "http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/v20150224/tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc"
    assert datasets[0]['last_modified'] == "2015-02-12T14:37:00Z"
    assert datasets[0]['title'] == "tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc"
    assert datasets[0]['resourcename'] == "/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/v20150224/tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc"
    assert datasets[0]['size'] == '5.0M'
