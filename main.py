import sys,os
import json
import urlparse
import urllib2 as urllib
import xml.etree.ElementTree as ET
from importlib import import_module
import argparse

def load_modules():
    module_names = ["modules."+f[:-3] for f in os.listdir("modules") if os.path.isfile(os.path.join("modules",f)) and f.split(".")[-1]=="py"];
    modules=[]
    for module_name in module_names:
        if module_name=="modules.__init__":
           continue
        try:
            modules.append(import_module(module_name).module)
        except AttributeError:
            print "\033[31mInvalid module "+module_name.split(".")[1]+"\033[m"  
    return modules

def get_page_urls(url,sitemap_name="sitemap.xml"):
    url=get_single_url(url,sitemap_name)
    sitemap_data=urllib.urlopen(url).read()        
    urls=[]
    root=ET.fromstring(sitemap_data)
    for sitemap in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"):
        for sitemap in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            urls.append(get_page_urls(url))
    for url in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        urls.append(url.text)
    return urls

def get_single_url(url,page):
    if not "//" in url:
        url="http://"+url
    url=urlparse.urljoin(url,page)
    return url

def get_data_from_page(pageurl):
    return urllib.urlopen(pageurl).read()

modules=load_modules()
pageurls=[]

def main(domain,module_names,**kwargs):
    out_data={}
    loaded_modules=[]
    page=None
    sitemap="sitemap.xml"
    if "page" in kwargs:
        page=kwargs["page"]
    if "sitemap" in kwargs:
        sitemap=kwargs["sitemap"]
    if page==None:
        pageurls = get_page_urls(domain,sitemap)
    else:
        pageurls = [get_single_url(domain,page)]
    for module in modules:
        if module.name in module_names:
            loaded_modules.append(module)
            module_names.remove(module.name)
    if len(module_names) > 0:
        print "\033[31mMissing modules" +str (module_names) +'\033[m'
    for module in loaded_modules:
        if module.runonce:
            print "Running module " + module.name
            try:
                out_data[module.name]=module.parse_page(get_data_from_page(get_single_url(domain,sitemap)),get_single_url(domain,sitemap))
            except Exception:
                out_data[module.name]=module.parse_page(get_data_from_page(get_single_url(domain,"/")),get_single_url(domain,"/"))
    for pageurl in pageurls:
        loc = out_data
        print "Working on page "+pageurl
        page_name=urlparse.urlparse(pageurl).path.split("/")[1:]
        for i in page_name:
            if not i in loc:
                loc[i] = {}
            loc=loc[i]
        try:
            page_data=get_data_from_page(pageurl)
        except UnicodeEncodeError:
            print "\033[31mNon-ascii character in page " + pageurl + ". Skipping...\033[m"
            continue 
        for module in loaded_modules:
            if(module.runonce):
                continue
            print "Running module "+module.name
            try:
                loc[module.name]=module.parse_page(page_data,pageurl)
            except Exception as e:
                print "\033[31mModule " + module.name + " could not parse page " + pageurl + ". Error: " + str(e) + "\033[m"
                loc[module.name]=module.parse_page(page_data,pageurl)

    with open("output.json","w") as f:
        json.dump(out_data,f)

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Scrape your website for various SEO-related information")
    parser.add_argument('domain', type=str, nargs=1)
    parser.add_argument('modules',type=str, nargs="+")
    parser.add_argument('-p',metavar='page',help="scrape a single page",nargs=1)
    parser.add_argument('-s',metavar='sitemap',help="define a custom location for the sitemap",nargs=1)
    args=parser.parse_args()
    page=None
    sitemap="sitemap.xml"
    if args.p:
        page=args.p[0]
    if args.s:
        sitemap=args.s[0]
    main(args.domain[0],args.modules,page=page,sitemap=sitemap)
