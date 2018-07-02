import urllib2,urlparse

class Robots:
    def __init__(self):
        self.runonce = True
        self.name="Robots"
    def parse_page(self,page_data,page_url):
        try:
            return urllib2.open(urlparse.urljoin(page_url,robots.txt))
        except Exception:
            return "NO_ROBOTS_TXT"
self.modules=Robots()
