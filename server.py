from bottle import route,run,request
import pprint
import json

@route("/",method='POST')
def index():
    data = request.body.read()
    try:
        x=json.loads(data)
    except ValueError:
        return {"error":"not_valid_json"} 
    try:
        domain = x["domain"]
    except KeyError:
        return {"error":"no_domain"}
    if "sitemap" in x.keys() and "page" in x.keys():
        return {"error":"invalid_"}
    
    args = {"domain":domain,"modules":["all"],"page":"","sitemap":"sitemap.xml","regex":"regex"}

    if "modules" in x.keys(): args.modules = x["modules"]
    if "page" in x.keys(): args.page = x["page"]
    if "sitemap" in x.keys(): args.sitemap = x["sitemap"]
    if "regex" in x.keys(): args.regex = x["regex"]

run(host='localhost',port=8080)
