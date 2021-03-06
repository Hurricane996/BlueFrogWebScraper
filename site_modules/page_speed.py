import json
import requests
import os


API_KEY=os.environ.get("PAGE-SPEED-KEY")

if not API_KEY
    raise ValueError("API key not set. Please set the environment variable PAGE-SPEED-KEY to a Google Page Speed API key")

# Stolen from stackoverfloe
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def run(page_url):
    request_url="https://www.googleapis.com/pagespeedonline/v4/runPagespeed?url=" + page_url + "&strategy=desktop&key=" + API_KEY
    result=requests.get(request_url).json()
    try:
        speedscore = result["ruleGroups"]["SPEED"]["score"]
        response_bytes=int(result["pageStats"]["overTheWireResponseBytes"])+int(result["pageStats"]["otherResponseBytes"])
    except KeyError:
        return "error"
    return {"score":speedscore,"size":sizeof_fmt(response_bytes)}
name="page_speed"
