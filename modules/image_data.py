from HTMLParser import HTMLParser

class ImageData(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.runonce=False
        self.name="image_data"
        self.url=""
        self.images=[]
        self.images_without_alt=[]
    def parse_page(self,page_data,page_url):
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
            if alt=="":
                self.images_without_alt.append({"src":src})
            else:
                self.images.append({"src":src,"alt":alt})
module=ImageData()
