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
    logger.debug(cat)
    return cat

def write_files(files):
    with open('names.csv', 'w') as csvfile:
        fieldnames = ['filename', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #writer.writeheader()
        for url in files:
            u = urlparse.urlsplit(url)
            filename = os.path.basename(u.path)
            writer.writerow({'filename': filename, 'url': url})

def crawl(page, depth=0):
    if depth < 0:
        return
    
    logger.debug('crawl page %s %d', page, depth)
    response = requests.head(page)
    if not 'text/html' in response.headers['content-type']:
        return
    response = requests.get(page)
    if not response.ok:
        return
    soup = BeautifulSoup(response.text)
    #print(soup.prettify())
    links = soup.find_all('a')
    newpages = set()
    newfiles = set()
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
                newfiles.add(url)
            else:
                newpages.add(url)
    write_files(newfiles)
    logger.debug('newpages %d', len(newpages))
    for page in newpages:
        crawl(page, depth=depth-1)
