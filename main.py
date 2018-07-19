#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser(description="tool that gets seo-related information by crawling website")

parser.add_argument("site",help="the website you want to run the scraper on")
parser.add_argument("modules",help="the modules you wish to load, or all for all of them",default="all",nargs="*");
group = parser.add_mutually_exclusive_group()
group.add_argument("-p","--page",help="run the scraper on a single page instead of an entire site")
group.add_argument("-s","--sitemap",help="specify a custom sitemap location",default="sitemap.xml")

args=parser.parse_args()

print args.modules
