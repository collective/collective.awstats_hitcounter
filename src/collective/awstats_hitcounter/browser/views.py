from plone import api
from utils import counter
import json

class HitcounterView(object):

    def __call__(self):
        """returns the total count based on the query"""
        awstat_pattern = api.portal.get_registry_record(
                       'awstats_hitcounter.awstats_url_pattern')
        # we depend on a properly configured url pattern
        # which is in the docs
        site = api.portal.get()
        path = self._relative_path()

        self.request.response.setHeader("Content-type", "application/json")

        views = counter(path, awstat_pattern)
        if views <= 0:
            json_data = json.dumps({'success':'false'})
        else: 
            content_type = self.context.Type()
            creation_date = self.context.CreationDate()
            creation_date = site.toLocalizedTime(creation_date)
            modification_date = self.context.modified()
            modification_date = site.toLocalizedTime(modification_date)
 
            data = dict(success = "true",
                    creation_date = creation_date,
                    modification_date = modification_date,
                    page_views = views,
                    content_type = content_type)
            json_data = json.dumps(data)

        return json_data

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
