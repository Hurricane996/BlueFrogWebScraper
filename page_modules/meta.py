from HTMLParser import HTMLParser;

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
    def parse_page(self,page_data,page_url):
        self.description = ""
        self.keywords=[]
        self.title=""
        self.intitle=False
        self.feed(page_data.decode("utf8","ignore"))
        return {"description":self.description,"keywords":self.keywords,"title":self.title};
    def handle_starttag(self,tag,attrs):
        if tag=="meta":
            self.handle_startendtag(tag,attrs)
        if tag=="title":
            self.intitle=True

    def handle_startendtag(self,tag,attrs):
        if tag=="meta":
            name=""
            content=""
            for attr in attrs:
                if attr[0]=="name" or attr[0]=="property":
                    name=attr[1]
                if attr[0]=="content":
                    content=attr[1]
            if name=="description":
                self.description=content
            if name=="keywords":
                print content.split(" ")
                self.keywords.extend(content.split(" "))
    def handle_endtag(self,tag):
        if tag=="title":
            self.intitle=False
    def handle_data(self,data):
        if self.intitle:
            self.title=data
parser=Parser()
def run(page_data,page_url):
    return parser.parse_page(page_data,page_url)
name="meta"

