import requests
from HTMLParser import HTMLParser
import urlparse
from utils import sizeof_fmt


class ImageDataAdvanced(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.runonce=False
        self.session=requests.Session()
        self.session.trust_env=False
        self.name="image_data_advanced"
        self.images=[]
    def parse_page(self,page_data,page_url):
        self.images=[]
        self.url=page_url
        if(page_url[-4:]==".pdf"):
            return {}
        self.feed(page_data.decode("utf8","ignore"))
        return self.images
    def handle_startendtag(self,tag,attrs):
        if tag=="img":
            src=""
            for attr in attrs:
                if attr[0]=="src":
                    src=attr[1]
            req=self.session.get(urlparse.urljoin(self.url,src),headers={"Connection":"close"})
            length=int(req.headers["Content-Length"])
            self.images.append({"src":src,"size":sizeof_fmt(length)}) 
module = ImageDataAdvanced()  
