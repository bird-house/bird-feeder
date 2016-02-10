import nose
from nose.tools import ok_
from nose.tools import raises
from nose.plugins.attrib import attr

from birdfeeder import walker

from tests.common import TESTDATA, TESTDATA_PATH

def test_dataset():
    ds = walker.Dataset(TESTDATA['cordex_tasmax.nc'], basedir=TESTDATA_PATH)
    
    print ds.size

    assert ds.name == 'tasmax_EUR-44_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200602-200612.nc'
    assert 'tasmax' in ds.variable
    assert ds.last_modified == '2015-05-06T13:22:33Z'
    assert ds.content_type == 'application/netcdf'
    assert 'tasmax' in ds.url
    assert ds.path == '/CORDEX/EUR-44/mon/tasmax_EUR-44_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200602-200612.nc'
    assert ds.size == '301.2K'


def test_crawl():
    datasets = [ds for ds in walker.crawl(start_dir=TESTDATA_PATH)]
    assert len(datasets) == 1
    assert ds.name == 'tasmax_EUR-44_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200602-200612.nc'
    
