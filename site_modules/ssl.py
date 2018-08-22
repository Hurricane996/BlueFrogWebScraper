import requests
import urllib2 as urllib
import traceback

def run(page_url):
    try:
        if page_url[:7]=="http://":
            page_url="https://"+page_url[7:]
        requests.head(page_url,timeout=3,verify=True)
        return {"ssl":True}
    except requests.exceptions.Timeout:
        return {"ssl":False}
    except requests.SSLError:
        return {"ssl":Falsegy}
    except requests.exceptions.ConnectionError as e:
        return {"ssl":False}
name="ssl"
