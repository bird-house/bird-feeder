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

def write_datasets(page, depth=0, filename='out.csv'):
    with open(filename, 'w') as csvfile:
        fieldnames = ['name', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for ds in crawl(page, depth):
            writer.writerow({'name': ds.name, 'url': ds.url})

class Dataset(object):
    """
    Abstract dataset class
    """
    def __init__(self, url):
        self.url = url

        u = urlparse.urlsplit(url)
        self.name = os.path.basename(u.path)

def crawl(page, depth=0):
    logger.debug('crawl page %s %d', page, depth)
    response = requests.head(page)
    if not 'html' in response.headers['content-type']:
        raise Exception('Crawler accepts only HTML pages, got {0}'.format(response.headers['content-type']))
    response = requests.get(page)
    if not response.ok:
        raise Exception('Failed to access page {0}'.format(page))
    soup = BeautifulSoup(response.text)
    #print(soup.prettify())
    links = soup.find_all('a')
    newpages = set()
    datasets = []
    for link in links:
        if ('href' in dict(link.attrs)):
            if link.text.strip().lower() in ['name', 'last modified', 'size', 'description', 'parent directory']:
                continue
            url = construct_url(page, link.attrs['href'])
            if url.find("'")!=-1:
                continue
            url=url.split('#')[0] # remove location portion
            #if url[0:4]=='http' and not self.is_in_url_list(url):
            #if 'application/x-netcdf' in response.headers['content-type']:
            if url.endswith('.nc'):
                datasets.append(Dataset(url))
            else:
                newpages.add(url)
    for ds in datasets:
        yield ds
    if depth > 0:
        for page in newpages:
            for ds in crawl(page, depth=depth-1):
                yield ds
