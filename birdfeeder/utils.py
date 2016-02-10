import math

def humanize_filesize(size):
    """
    natural filesize.

    taken from: http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    see also: https://pypi.python.org/pypi/humanize/
    """
    size = abs(size)
    if (size==0):
        return "0B"
    units = ['B','K','M','G','T','P','E','Z','Y']
    p = math.floor(math.log(size, 2)/10)
    return "%.1f%s" % (size/math.pow(1024,p),units[int(p)])
