from HTMLParser import HTMLParser
import utils
import requests

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.runonce=False
        self.name="image_data"
        self.url=""
        self.session=requests.Session()
        self.session.trust_env=False
    def parse_page(self,page_data,page_url):
        self.images=[]
        self.images_without_alt=[]
        if(page_url[-4:]==".pdf"):
            return {}
        self.url=page_url
        self.feed(page_data.decode("utf8","ignore"))
        return {
                    "images":self.images,
                    "images_without_alt":self.images_without_alt,
                    "num_images_without_alt":len(self.images_without_alt)
               } 
    def handle_starttag(self,tag,attrs):
        if tag=="img":
            self.handle_startendtag(tag,attrs)
    def handle_endtag(*a):
        pass
    def handle_startendtag(self,tag,attrs):
        if tag=="img":
            src=""
            alt=""
            for attr in attrs:
                if attr[0]=="src":
                    src=attr[1]
                if attr[0]=="alt":
                    alt=attr[1]
            req=self.session.get(urlparse.urljoin(self.url,src),headers={"Connection":"close"})
            length=int(req.headers["Content-Length"])
            if alt=="":
                self.images_without_alt.append({"src":src,"size":utils.sizeof_fmt(length)})
            else:
                self.images.append({"src":src,"alt":alt,"size":utils.sizeof_fmt(length)})
parser=Parser()
def run(page_data,page_url):
    return parser.parse_page(page_data,page_url)
name="image_data"
