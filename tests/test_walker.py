import nose
from nose.tools import ok_
from nose.tools import raises
from nose.plugins.attrib import attr

from birdfeeder import walker

def test_dataset():
    #raise SkipTest
    ds = walker.Dataset("/home/pingu/sandbox/birdhouse/flyingpigeon/tests/testdata/cordex/tasmax_EUR-44_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200602-200612.nc")
    
    print ds

    assert ds.name == 'tasmax_EUR-44_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1_mon_200602-200612.nc'
    assert 'tasmax' in ds.variable
    assert ds.last_modified == '2015-05-06T13:22:33Z'
    assert ds.content_type == 'application/netcdf'
    assert 'tasmax' in ds.url
    assert 'tasmax' in ds.path
    assert ds.size == ''
    
    
