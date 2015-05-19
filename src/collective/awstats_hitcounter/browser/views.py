import requests
import lxml.html as LH
from StringIO import StringIO
from plone import api

class HitcounterView(object):

    def __call__(self):
        """returns the total count based on the query"""
        awstat_pattern = api.portal.get_registry_record(
                       'awstats_hitcounter.awstats_url_pattern')
     
        path = self._relative_path()
        hit_url = awstat_pattern.format(path)
        print hit_url
        context_path = self.context.getPhysicalPath()
        r = requests.get(hit_url)
        tree = LH.parse(StringIO(r.text))
   
        total_hits = '0'

        # xpath that checks if this path exists in awstats
        page_url_count_text = tree.xpath("//th")[0].text_content()
        page_url_count = page_url_count_text.split(': ')[1].split(' ')[0]
        page_url_count = int(page_url_count)
        if page_url_count > 0:
            # xpath that wrangles the total hits
            total_hits = tree.xpath("//td")[-5].text
            return total_hits
        return total_hits

    def _relative_path(self):
        """ Get site root relative path to an item
    
        @return: Path to the context object, relative to site root, 
        prefixed with a slash.
        """
    
        portal = api.portal.get()
    
        site_path = portal.getPhysicalPath();
        context_path = self.context.getPhysicalPath()
    
        relative_path = context_path[len(site_path):]
    
        return "/" + "/".join(relative_path)
