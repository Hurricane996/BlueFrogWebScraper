import urllib2,urlparse

def run(self,page_url):
    try:
       return urllib2.urlopen(urlparse.urljoin(page_url,"robots.txt")).read()
    except Exception:
       return "NO_ROBOTS_TXT"
