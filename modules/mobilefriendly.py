import requests,json
import traceback

API_KEY="AIzaSyDQv5wGmKstVbBBZr5lyZ8t9kItfHvWqos"

class PageSpeed:
    def __init__(self):
        self.name="mobilefriendly"
        self.runonce=True
    def parse_page(self,page_data,page_url):
        page_url="/".join(page_url.split("/")[:-1])+"/"
        request_url="https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?fields=mobileFriendliness&key="+API_KEY
        result=requests.post(request_url,data={"url":page_url})
        try:
            rson = result.json()
            return rson["mobileFriendliness"]=="MOBILE_FRIENDLY"
        except ValueError:
            print [a for a in result.iter_lines()]
            return "ERROR"
        except Exception:
            return {"ERROR":result.json()}
module=PageSpeed()

