import nose
from nose.tools import ok_
from nose.plugins.attrib import attr

from birdfeeder.utils import humanize_filesize

def test_humanize_filesize():
    print humanize_filesize(20000000)
    assert humanize_filesize(256) == '256.0B'
    assert humanize_filesize(1024) == '1.0K'
    assert humanize_filesize(1048576) == '1.0M'
    assert humanize_filesize(2000000) == '1.9M'
    assert humanize_filesize(157286400) == '150.0M'
    assert humanize_filesize(20000000) == '19.1M'
    assert humanize_filesize(1073741824) == '1.0G'
    assert humanize_filesize(5000000000) == '4.7G'

    
