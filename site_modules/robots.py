import urllib2,urlparse

def run(page_url):
    try:
       return {"robots":urllib2.urlopen(urlparse.urljoin(page_url,"robots.txt")).read()}
    except Exception:
        return {"robots":"NO_ROBOTS_TXT"}
name="robots"
