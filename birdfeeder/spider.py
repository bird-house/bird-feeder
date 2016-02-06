import sys
import os
import urlparse
from bs4 import BeautifulSoup 
import requests

found_files = set()

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
    print cat
    return cat

def add_file(url):
    found_files.add(url)

def crawl(page, depth=0):
    if depth < 0:
        return
    
    print 'crawl page', page, depth
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
                add_file(url)
            else:
                newpages.add(url)
            #print url
    print 'newpages', len(newpages)
    for page in newpages:
        crawl(page, depth=depth-1)


def main():
    page = "http://ensemblesrt3.dmi.dk/data/CORDEX/AFR-44/KNMI/MOHC-HadGEM2-ES/rcp45/r1i1p1/KNMI-RACMO22T/v1/mon"
    crawl(page=page, depth=3)

    print "result"
    for url in found_files:
        print url
            
if __name__ == '__main__':
    sys.exit(main())
