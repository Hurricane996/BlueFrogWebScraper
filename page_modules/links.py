from HTMLParser import HTMLParser
import requests
import urlparse

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.session=requests.Session()
        self.session.trust_env=False
    def parse_page(self,page_data,page_url):
        self.intlinks={"count":0,"links":[]}
        self.extlinks={"count":0,"links":[]}
        self.deadlinks={"count":0,"links":[]}
        self.url=page_url
        self.feed(page_data.decode("utf8","ignore"))
        return {"internal_links":self.intlinks,"external_links":self.extlinks,"dead_links":self.deadlinks}
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            self.handle_startendtag(tag,attrs)
    def handle_startendtag(self,tag,attrs):
        if tag=="a":
            src=""
            for attr in attrs:
                if attr[0]=="href":
                    src=attr[1]
            if src.split(":")[0] in ["mailto","tel"]:
                return
            src=urlparse.urljoin(self.url,src)
            if urlparse.urlparse(src).netloc.replace("www.","") == urlparse.urlparse(self.url).netloc.replace("www.",""):
                self.intlinks["count"]+=1
                self.intlinks["links"].append(src)
            else:
                self.extlinks["count"]+=1
                self.extlinks["links"].append(src)
            if src in self.intlinks:
                response=self.session.head(src)
                if response.status_code > 399:
                    self.deadlinks["count"]+=1
                    self.deadlinks["links"].append(src)
parser=Parser()
def run(page_data,page_url):
    return parser.parse_page(page_data,page_url)
name="links"
