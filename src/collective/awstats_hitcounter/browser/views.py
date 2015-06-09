from plone import api
from utils import counter
import json

#import requests
#import lxml.html as LH
#from StringIO import StringIO

class HitcounterView(object):

    def __call__(self):
        """returns the total count based on the query"""
        awstat_pattern = api.portal.get_registry_record(
                       'awstats_hitcounter.awstats_url_pattern')
        # we depend on a properly configured url pattern
        # which is in the docs
        path = self._relative_path()
        views = counter(path, awstat_pattern)
        content_type = self.context.Type()
        creation_date = self.context.CreationDate()
        data = dict(creation_date=creation_date,
                    total_views = views,
                    content_type = content_type)
        return json.dumps(data)

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
