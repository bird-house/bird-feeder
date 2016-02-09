import nose
from nose.tools import ok_
from nose.plugins.attrib import attr

from birdfeeder import spider

@attr('online')
def test_crawl_dmi_1():
    page="http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax"
    result = [ds for ds in spider.crawl(page, depth=0)]
    assert len(result) == 0

@attr('online')
def test_crawl_dmi_2():
    page="http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/"
    result = [ds for ds in spider.crawl(page, depth=1)]
    assert len(result) > 0
    assert 'tasmax' in result[0].name
    assert result[0].url.startswith(page)

@attr('online')
def test_write_datasets():
    page="http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/"
    spider.write_datasets(page, depth=1, filename="/tmp/out.csv")
