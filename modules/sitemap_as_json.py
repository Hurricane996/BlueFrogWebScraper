import urlparse
import xml.etree.ElementTree as ET

def get_page_urls(page_data):
    urls=[]
    root=ET.fromstring(page_data)
    for sitemap in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"):
        for sitemap in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            urls.append(get_page_urls(url))
    for url in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        urls.append(url.text)
    return urls
def re_d_str(the_dict):
    if the_dict == {}:
        return ""
    return {k : re_d_str(v) for k,v in the_dict.items()}
        


class SitemapAsJSON:
    def __init__(self):
        self.name="sitemap_as_json"
        self.runonce=True
    def parse_page(self,page_data,page_url):
        a={}
        for pageurl in get_page_urls(page_data):
            loc=a
            page_name=urlparse.urlparse(pageurl).path.split("/")[1:]
            for i in page_name:
                if not i in loc:
                    loc[i] = {}
                loc=loc[i];
         
        return re_d_str(a) 
module=SitemapAsJSON()
