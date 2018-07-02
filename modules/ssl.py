import requests
import urllib2 as urllib
import traceback

class SSL:
    def __init__(self):
        self.name="ssl"
        self.runonce=True
    def parse_page(self,page_data,page_url):
        try:
            if page_url[:7]=="http://":
                page_url="https://"+page_url[7:]
            requests.head(page_url,timeout=3,verify=True)
            return {"ssl":True,"ssl_root":True}
        except requests.exceptions.Timeout:
            try:
                page_url="https://www."+page_url[8:]
                requests.head(page_url,timeout=3,verify=True)
                return {"ssl":True,"ssl_root":False}
            except requests.exceptions.ConnectionError:
                return {"ssl":False,"ssl_root":False}
        except requests.exceptions.ConnectionError as e:
            traceback.print_exc()
            return {"ssl":False,"ssl_root":False}
module=SSL()
