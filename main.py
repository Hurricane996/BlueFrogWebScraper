#!/usr/bin/python

import argparse
import sys,os
import pprint


from page_modules import heading_grabber
from page_modules import image_data
from page_modules import links
from page_modules import meta

from site_modules import mobilefriendly
from site_modules import page_speed
from site_modules import robots
from site_modules import ssl

page_modules=[
    heading_grabber,
    image_data,
    links,
    meta
]

site_modules=[
    mobilefriendly,
    page_speed,
    robots,
    ssl 
]



def run_site_modules(domain,site_modules):
    for module in site_modules:
        data=module.run(domain)
        insert_site_data(domain,module.name,data)
def run_page_modules(domain,page_name,page_data,page_modules):
    for module in page_modules:
        data=module.run(domain,page_name,page_data)
        insert_page_data(domain,page_name,module.name,data)
def load_modules(module_names,loadable_modules):
    loaded_modules=[]
    for module in loadable_modules:
        if module.name in module_names:
            loaded_modules.append(module)
    return loaded_modules


def main(args):
    loaded_site_modules=load_modules(args.modules,page_modules)
    loaded_page_modules=load_modules(args.modules,site_modules)

if __name__='__main__'
    parser = argparse.ArgumentParser(description="tool that gets seo-related information by crawling website")

    parser.add_argument("site",help="the website you want to run the scraper on")
    parser.add_argument("modules",help="the modules you wish to load, or all for all of them",default="all",nargs="*");
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p","--page",help="run the scraper on a single page instead of an entire site")
    group.add_argument("-s","--sitemap",help="specify a custom sitemap location",default="sitemap.xml")

    args=parser.parse_args()
    main(args)
