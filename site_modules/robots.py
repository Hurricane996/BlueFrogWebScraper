import urllib2,urlparse

def run(page_url):
    try:
       return urllib2.urlopen(urlparse.urljoin(page_url,"robots.txt")).read()
    except Exception:
       return "NO_ROBOTS_TXT"
name="robots"
