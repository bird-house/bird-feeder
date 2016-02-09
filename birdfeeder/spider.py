import sys
import os
import urlparse
from bs4 import BeautifulSoup 
import requests
import csv

import logging
logger = logging.getLogger(__name__)

class InvalidPage(Exception):
    pass

def construct_url(url, href):
    u = urlparse.urlsplit(url.strip('/'))
    base_url = u.scheme + "://" + u.netloc
    relative_path = urlparse.urljoin(base_url, u.path)

    if href[0] == "/":
        # Absolute paths
        cat = urlparse.urljoin(base_url, href)
    elif href[0:4] == "http":
        # Full HTTP links
        cat = href
    else:
        # Relative paths.
        cat = relative_path + "/" + href
    #logger.debug(cat)
    return cat

def write_datasets(url, depth=0, filename='out.csv'):
    logger.info('Starting crawler ...')
    with open(filename, 'w') as csvfile:
        fieldnames = ['url', 'name', 'last_modified', 'size']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        ds_counter = 0
        for ds in crawl(url, depth):
            writer.writerow({'url': ds.url,
                             'name': ds.name,
                             'last_modified': ds.last_modified,
                             'size': ds.size})
            if ds_counter > 0 and ds_counter % 5000 == 0:
                logger.info('{0} datasets written ...'.format(ds_counter))
            ds_counter += 1
    logger.info('{0} datasets written to {1}'.format(ds_counter, filename))

class Dataset(object):
    def __init__(self, url, name=None, last_modified=None, size=None):
        self.url = url
        self.name = name
        self.last_modified = last_modified
        self.size = size

        if name is None:
            u = urlparse.urlsplit(url)
            self.name = os.path.basename(u.path)

class Page(object):
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self._parse_page()

    def _parse_page(self):
        links = self.soup.find_all('a')
        strlist = [s for s in self.soup.stripped_strings]
        newpages = set()
        self.datasets = []
        for link in links:
            if ('href' in dict(link.attrs)):
                if link.text.strip().lower() in ['name', 'last modified', 'size', 'description', 'parent directory']:
                    continue
                url = construct_url(self.url, link.attrs['href'])
                if url.find("'")!=-1:
                    continue
                url=url.split('#')[0] # remove location portion
                #if url[0:4]=='http' and not self.is_in_url_list(url):
                #if 'application/x-netcdf' in response.headers['content-type']:
                if url.endswith('.nc'):
                    # TODO: ugly parsing ...
                    try:
                        name = link.text.strip()
                        index = strlist.index(name)
                        attr = strlist[index+1].split()
                        last_modified = "{0}T{1}".format(attr[0], attr[1])
                        size = attr[2]
                        self.datasets.append(Dataset(url, name, last_modified, size))
                    except:
                        msg = "Could not parse dataset: {url}".format(url)
                        logger.exception(msg)
                        raise Exception(msg)
                else:
                    newpages.add(url)
        self.references = list(newpages)

def read_url(url):
    response = requests.head(url)
    if not 'content-type' in response.headers:
        raise InvalidPage('No content-type found in response header.')
    if not 'html' in response.headers['content-type']:
        raise InvalidPage('Crawler accepts only HTML pages, got {0}'.format(response.headers['content-type']))
    response = requests.get(url)
    if not response.ok:
        raise Exception('Failed to access page {0}'.format(url))
    return read_xml(response.text, url)

def read_xml(xml, baseurl):
    soup = BeautifulSoup(xml)
    #print(soup.prettify())
    return Page(soup, baseurl)
    
def crawl(url, depth=0):
    logger.debug('crawling page %s. depth=%d', url, depth)
    try:
        page = read_url(url)
    except InvalidPage:
        logger.exception("Skipped invalid page {0}".format(url))
    else:
        for ds in page.datasets:
            yield ds
        if depth > 0:
            for page in page.references:
                for ds in crawl(page, depth=depth-1):
                    yield ds
