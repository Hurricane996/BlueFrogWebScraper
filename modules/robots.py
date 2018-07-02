import urllib2,urlparse

class Robots:
    def __init__(self):
        self.runonce = True
        self.name="robots"
    def parse_page(self,page_data,page_url):
        try:
           return urllib2.urlopen(urlparse.urljoin(page_url,"robots.txt")).read()
        except Exception:
           return "NO_ROBOTS_TXT"
module=Robots()
