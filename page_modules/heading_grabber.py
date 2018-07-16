from HTMLParser import HTMLParser

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.runonce=False
        self.name="heading_grabber"
    def parse_page(self,page_data,page_url):
        if(page_url[-4:]==".pdf"):
            return {}
        self.hcount={
                        "h1":{"count":0,"text":[]},
                        "h2":{"count":0,"text":[]},
                        "h3":{"count":0,"text":[]},
                        "h4":{"count":0,"text":[]},
                        "h5":{"count":0,"text":[]},
                        "h6":{"count":0,"text":[]}
                    }
        self.inh1=False
        self.inh2=False
        self.inh3=False
        self.inh4=False
        self.inh5=False
        self.inh6=False

        self.feed(page_data.decode("utf8","ignore"))
        return self.hcount
    def handle_starttag(self,tag,attrs):
        if tag=="h1":
            self.hcount["h1"]["count"]+=1
            self.inh1=True
        elif tag=="h2":
            self.hcount["h2"]["count"]+=1
            self.inh2=True
        elif tag=="h3":
            self.hcount["h3"]["count"]+=1
            self.inh3=True
        elif tag=="h4":
            self.hcount["h4"]["count"]+=1
            self.inh4=True
        elif tag=="h5":
            self.hcount["h5"]["count"]+=1
            self.inh5=True
        elif tag=="h6":
            self.hcount["h6"]["count"]+=1
            self.inh6=True
    def handle_endtag(self,tag):
        if tag=="h1":
            self.inh1=False
        elif tag=="h2":
            self.inh2=False
        elif tag=="h3":
            self.inh3=False
        elif tag=="h4":
            self.inh4=False
        elif tag=="h5":
            self.inh5=False
        elif tag=="h6":
            self.inh6=False
    def handle_data(self,data):
        if self.inh1:
            self.hcount["h1"]["text"].append(data)
        if self.inh2:
            self.hcount["h2"]["text"].append(data)
        if self.inh3:
            self.hcount["h3"]["text"].append(data)
        if self.inh4:
            self.hcount["h4"]["text"].append(data)
        if self.inh5:
            self.hcount["h5"]["text"].append(data)
        if self.inh6:
            self.hcount["h6"]["text"].append(data)
parser=Parser()
def run(page_data,page_url):
    parser.run(page_data,page_url)
