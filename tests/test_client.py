import nose
from nose.plugins.attrib import attr

from birdfeeder import client

@attr('online')
def test_write_spider():
    page="http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/"
    client.write_spider(page, depth=1, filename="/tmp/out.csv")
