import urlparse
import urllib2 as urllib
import xml.etree.ElementTree as ET


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
    req=urllib.Request(pageurl,headers={"User-Agent":"pybot"})
    return urllib.urlopen(req).read()

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def dataToXML(d,roottag="data"):
    r = ET.Element(roottag)
    return ET.tostring(buildxml(r,d),pretty_print=True)

def buildxml(r, d):
    if isinstance(d, dict):
        for k, v in d.iteritems():
            s = ET.SubElement(r, k)
            buildxml(s, v)
    elif isinstance(d, tuple) or isinstance(d, list):
        for v in d:
            s = ET.SubElement(r, 'i')
            buildxml(s, v)
    elif isinstance(d, basestring):
        r.text = d
    else:
        r.text = str(d)
    return r
