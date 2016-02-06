import nose
from nose.tools import ok_
from nose.plugins.attrib import attr

from birdfeeder import spider

@attr('online')
def test_crawl_dmi_0():
    spider.crawl(page="http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon", depth=0)
