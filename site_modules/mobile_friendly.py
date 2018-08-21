import requests,json
import traceback

API_KEY="AIzaSyDQv5wGmKstVbBBZr5lyZ8t9kItfHvWqos"

def run(page_url):
    request_url="https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?fields=mobileFriendliness&key="+API_KEY
    result=requests.post(request_url,data={"url":page_url})
    try:
        rson = result.json()
        return {"mobile_friendly":rson["mobileFriendliness"]=="MOBILE_FRIENDLY"}
    except ValueError:
        print [a for a in result.iter_lines()]
        return {"err":True}
    except Exception:
        return {"err":result.json()}
name="mobile_friendly"
