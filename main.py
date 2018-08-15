#!/usr/bin/python

import argparse
import sys,os

import re

import mysql

import json
import xml.etree.ElementTree as ET

import urlparse
import urllib2

from page_modules import heading_grabber
from page_modules import image_data
from page_modules import links
from page_modules import meta

from site_modules import mobile_friendly
from site_modules import page_speed
from site_modules import robots
from site_modules import ssl

FAILURE_REGEX="a^"

page_modules=[
    heading_grabber,
    image_data,
    links,
    meta
]

site_modules=[
    mobile_friendly,
    page_speed,
    robots,
    ssl 
]

def open_url(url):
    req=urllib2.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    return urllib2.urlopen(req).read()


def run_site_modules(domain,site_modules):
    for module in site_modules:
        print module.__name__
        data=json.dumps(module.run(domain))
        mysql.insert_site_data(domain,module.name,data)
def run_page_modules(domain,page_url,page_data,page_modules):
    if page_url[-1]=="/":
        page_url=page_url[:-1]
    page_name=page_url.split("/")[-1]
    for module in page_modules:
        print module.__name__
        data=json.dumps(module.run(page_data,page_url))
        mysql.insert_page_data(domain,page_name,module.name,data)


def load_modules(module_names,loadable_modules):
    loaded_modules=[];
    for module in loadable_modules:
        if module.name in module_names:
            loaded_modules.append(module)
    return loaded_modules

def get_pages(site,sitemap,regex,max_urls):
    urls=[]

    print regex

    url=urlparse.urljoin(site,sitemap)
    data=open_url(url)
    
    root= ET.fromstring(data)     

    """for sitemap in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"):
        for sitemap in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            urls.append(get_pages(site,urlparse.urlparse(url).path))"""
    for url in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        if url.text and (re.search(regex,url.text)==None):
            urls.append(url.text)
    urls=urls[:max_urls]
    return urls

def build_page_structure_in_db(site_name,urls):
    print sorted(urls,key=lambda u:len(urlparse.urlparse(u).path.split("/")))
    for page_url in urls:
        print "Adding page "+page_url+" to db"
        page_name=urlparse.urlparse(page_url).path.split("/")[-1]
        page_path=urlparse.urlparse(page_url).path.split("/")
        if not mysql.page_exists(site_name,page_path[0]):
            mysql.add_page(page_path[0],site_name)
        if len(page_path)>1:
            n=0
        
            for i in page_path[1:]:
                n+=1
                if not mysql.page_exists(site_name,page_path[n]):
                    mysql.add_page(page_path[n],site_name,page_path[n-1])
    
    
def main(args):
    mysql.initialize()
    
    print args.modules
     
    if args.modules[0]=="all":
        loaded_site_modules=site_modules
        loaded_page_modules=page_modules
    else:
        loaded_site_modules=load_modules(args.modules,site_modules)
        loaded_page_modules=load_modules(args.modules,page_modules)

    if not args.page:
        pages=get_pages(args.site,args.sitemap,args.exclude_regex,55)
        build_page_structure_in_db(args.site,pages)

    run_site_modules(args.site,loaded_site_modules)
     
    if not args.page:
        for page in pages:
            print "Working on page " + page
            page_data=open_url(page)
            run_page_modules(args.site,page,page_data,loaded_page_modules)
    else:
        page=urlparse.urljoin(args.site,args.page)
        page_data=open_url(page)
        run_page_modules(args.site,page,page_data,loaded_page_modules)
        

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="tool that gets seo-related information by crawling website")

    parser.add_argument("site",help="the website you want to run the scraper on")
    parser.add_argument("modules",help="the modules you wish to load, or all for all of them",default=["all"],nargs="*");
    parser.add_argument("-r","--exclude-regex",help="Specify a regex that, when any part of it is matched, excludes that URL",default=FAILURE_REGEX)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p","--page",help="run the scraper on a single page instead of an entire site")
    group.add_argument("-s","--sitemap",help="specify a custom sitemap location",default="sitemap.xml")

    args=parser.parse_args()
    main(args)
