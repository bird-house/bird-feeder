import nose
from nose.tools import ok_
from nose.tools import raises
from nose.plugins.attrib import attr

from birdfeeder import spider

@attr('online')
@raises(spider.InvalidPage)
def test_invalid_page():
    page = "http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/ICHEC-EC-EARTH/rcp45/r1i1p1/KNMI-RACMO22T/v1/day/snc/Daily_snc_CC.ascii"
    spider.read_url(page)

@attr('online')
@raises(spider.InvalidPage)
def test_no_html():
    page = "http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/v20150224/tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc"
    spider.read_url(page)

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


def test_read_xml_dmi_1():
    xml = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
  <head>
    <title>Index of /data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax</title>
  </head>
  <body>
    <h1>Index of /data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax</h1>
    <pre>
      <img src="/icons/blank.gif" alt="Icon "> 
      <a href="?C=N;O=D">Name</a>                                                                        
      <a href="?C=M;O=A">Last modified</a>      
      <a href="?C=S;O=A">Size</a>  
      <a href="?C=D;O=A">Description</a>
      <hr>
      <img src="/icons/back.gif" alt="[PARENTDIR]"> 
      <a href="/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/">Parent Directory</a>
      <img src="/icons/folder.gif" alt="[DIR]"> 
      <a href="v20150224/">v20150224/</a>  
      2015-02-24 14:10    -   
      <hr>
    </pre>
    <address>Apache/2.4.7 (Ubuntu) Server at ensemblesrt3.dmi.dk Port 80</address>
  </body>
</html>
    """
    page_url = "http://nowhere.org/cordex/"
    page = spider.read_xml(xml, baseurl=page_url)
    assert len(page.datasets) == 0
    assert len(page.references) == 1
    assert page.references[0].startswith(page_url)
    
def test_read_xml_dmi_2():
    xml = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
  <head>
    <title>Index of /data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/v20150224</title>
  </head>
  <body>
    <h1>Index of /data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/v20150224</h1>
    <pre>
      <img src="/icons/blank.gif" alt="Icon "> <a href="?C=N;O=D">Name</a> <a href="?C=M;O=A">Last modified</a> <a href="?C=S;O=A">Size</a> <a href="?C=D;O=A">Description</a>
      <hr>
      <img src="/icons/back.gif" alt="[PARENTDIR]"> 
      <a href="/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon/tasmax/">Parent Directory</a> 
      -  
      <img src="/icons/unknown.gif" alt="[   ]"> <a href="tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc">tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc</a> 2015-02-12 14:37  5.0M  
      <img src="/icons/unknown.gif" alt="[   ]"> <a href="tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_201101-202012.nc">tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_201101-202012.nc</a> 2015-02-12 14:37  9.9M
      <hr>
    </pre>
    <address>Apache/2.4.7 (Ubuntu) Server at ensemblesrt3.dmi.dk Port 80</address>
  </body>
</html>
    """
    page_url = "http://nowhere.org/cordex/"
    page = spider.read_xml(xml, baseurl=page_url)
    assert len(page.datasets) == 2
    assert len(page.references) == 0
    for ds in page.datasets:
        assert ds.url.startswith(page_url)
        assert 'tasmax' in ds.url
    assert page.datasets[0].ID == "tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc"
    assert page.datasets[0].name == "tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc"
    assert page.datasets[0].last_modified == "2015-02-12T14:37:00Z"
    assert page.datasets[0].size == "5.0M"
    assert page.datasets[0].url == "http://nowhere.org/cordex/tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc"
    assert page.datasets[0].download_url == "http://nowhere.org/cordex/tasmax_AFR-44_MOHC-HadGEM2-ES_rcp45_r1i1p1_KNMI-RACMO22T_v1_mon_200601-201012.nc"

