from plone import api
from utils import counter
import json
import Acquisition
from zope.component import getUtility, getMultiAdapter

from collective.awstats_hitcounter.portlet.portlets import IPopularContentPortlet
from plone.portlets.interfaces import IPortletRetriever, IPortletManager

from collective.awstats_hitcounter.browser.utils import filter_urls
from collective.awstats_hitcounter.browser.utils import get_urls

class PopularContentPortletActive(object):
    def __call__(self):
        """ return true if the popular content portlet is active """
        for column in ["plone.leftcolumn", "plone.rightcolumn"]:

            manager = getUtility(IPortletManager, name=column)
            retriever = getMultiAdapter((self.context, manager), IPortletRetriever)
            portlets = retriever.getPortlets()

        for portlet in portlets:
        # Identify portlet by interface provided by assignment
            if IPopularContentPortlet.providedBy(portlet["assignment"]):
                return True

        return False



class HitcounterView(object):

    def __call__(self):
        """returns the total count based on the query"""
        awstat_pattern = api.portal.get_registry_record(
                       'awstats_hitcounter.awstats_url_pattern')
        # we depend on a properly configured url pattern
        # which is in the docs
        site = api.portal.get()
        path = self._relative_path()
        downloads = None
        self.request.response.setHeader("Content-type", "application/json")
        if self.context.portal_type == "File":
            downloads = counter("{0}/at_download/file".format(path),
                                awstat_pattern)
        views = counter(path, awstat_pattern)
        hits = counter(path, awstat_pattern, hits=True)
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
                    hits = hits,
                    content_type = content_type)
            if downloads:
                data['downloads'] = downloads
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

class PopularContentView(object):

    @property
    def popular_content_items(self):
        """
        Return the popular content
        for the browser view
        """
        # The following values are available via the global registry:
        # url_of_popular_page,prevent_direct_downloads
        # black_list,type_white_list
        
        url_of_popular_page = api.portal.get_registry_record(
                            'awstats_hitcounter.url_of_popular_page')
        prevent_direct_downloads = api.portal.get_registry_record(
                            'awstats_hitcounter.prevent_direct_downloads')
        black_list = api.portal.get_registry_record(
                            'awstats_hitcounter.black_list')
        type_white_list = api.portal.get_registry_record(
                            'awstats_hitcounter.type_white_list')
        view_more_item_count = api.portal.get_registry_record(
                            'awstats_hitcounter.view_more_item_count')

 

        popular_urls = get_urls(url_of_popular_page,
                            black_list,
                            limit=view_more_item_count)
 
        return filter_urls(
                   popular_urls,type_white_list=type_white_list,
                   prevent_direct_downloads=prevent_direct_downloads
                    )
