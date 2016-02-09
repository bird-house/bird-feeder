import sys
import os
import urlparse
from bs4 import BeautifulSoup 
import requests
import csv

import logging
logger = logging.getLogger(__name__)

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
    with open(filename, 'w') as csvfile:
        fieldnames = ['name', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for ds in crawl(url, depth):
            writer.writerow({'name': ds.name, 'url': ds.url})

class Dataset(object):
    """
    Abstract dataset class
    """
    def __init__(self, url):
        self.url = url

        u = urlparse.urlsplit(url)
        self.name = os.path.basename(u.path)

class Page(object):
    def __init__(self, soup, url):
        self.soup = soup
        self.url = url
        self._parse_page()

    def _parse_page(self):
        links = self.soup.find_all('a')
        self.references = set()
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
                    self.datasets.append(Dataset(url))
                else:
                    self.references.add(url)

def read_url(url):
    response = requests.head(url)
    if not 'html' in response.headers['content-type']:
        raise Exception('Crawler accepts only HTML pages, got {0}'.format(response.headers['content-type']))
    response = requests.get(url)
    if not response.ok:
        raise Exception('Failed to access page {0}'.format(url))
    return read_xml(response.text, url)

def read_xml(xml, baseurl):
    soup = BeautifulSoup(xml)
    #print(soup.prettify())
    return Page(soup, baseurl)
    
def crawl(url, depth=0):
    logger.debug('crawl page %s %d', url, depth)
    page = read_url(url)
    
    for ds in page.datasets:
        yield ds
    if depth > 0:
        for page in page.references:
            for ds in crawl(page, depth=depth-1):
                yield ds
