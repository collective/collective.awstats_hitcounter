import urllib
import urlparse
from random import shuffle
from AccessControl import Unauthorized

from DateTime import DateTime
from zope.schema.fieldproperty import FieldProperty
from z3c.form import field
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api
#from plone.directives import form
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer


from collective.awstats_hitcounter.browser.utils import get_urls
from collective.awstats_hitcounter.browser.utils import blacklist

type_whitelist = ['News Item','Page','Link','File']
#import z3cformhelper  # XXX: Import from plone.app.portlets since Plone 4.3
import z3cformhelper


def _(x):
    """ Spoof gettext for now """
    return x


class IPopularContentPortlet(IPortletDataProvider):
#form.Schema):
    """
    Define popular content portlet fields.
    """
    portlet_name = schema.TextLine(title=_(u"Portlet Name"),
                           description=_(u"Add the name of the portlet here"),
                           required=True,
                           default=u"")

    items_to_show = schema.Int(title=_(u"Max Items to show"),
                           description=_(u"The maximum number of items that should be shown in the portlet"),
                           required=False,
                           default=3)

    url_of_popular_page = schema.TextLine(title=_(u"awstats popular content page"),
                           description=_(u"URL of the awstats page which shows popular content"),
                           required=False,
                           default=u"")

    prevent_direct_downloads = schema.Bool(title=_(u"Prevent Direct Downloads"),
                                   description=_(u"Prevent direct download of files"),
                                   default=True)

    black_list = schema.List(title=_(u"Blacklist"),
                           description=_(u"List of items that should not be returned as popular content"),
                           required=False,
                           value_type=schema.TextLine(title=_(u"item")),
                           default=blacklist)

    type_white_list = schema.List(title=_(u"Type White List"),
                           description=_(u"White list of types which should be retrieved as popular content"),
                           required=False,
                           value_type=schema.TextLine(title=_(u"item")),
                           default=type_whitelist)


    css = schema.TextLine(title=_(u"HTML styling"),
                          description=_(u"Extra CSS classes"),
                          required=False)


class Assignment(base.Assignment):

    implements(IPopularContentPortlet)

    # Make sure default values work correctly migration proof manner
    items_to_show = FieldProperty(IPopularContentPortlet["items_to_show"])
    portlet_name = FieldProperty(IPopularContentPortlet["portlet_name"])
    css = FieldProperty(IPopularContentPortlet["css"])
    prevent_direct_downloads = FieldProperty(IPopularContentPortlet["prevent_direct_downloads"])
    black_list = FieldProperty(IPopularContentPortlet["black_list"])
    type_white_list = FieldProperty(IPopularContentPortlet["type_white_list"])
    url_of_popular_page = FieldProperty(IPopularContentPortlet["url_of_popular_page"])
 

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def modified(self):
        """
        (cache busting)
        """
        return DateTime(self._p_mtime)

    @property
    def title(self):
        """
        Be smart as what show as the management interface title.
        """
        entries = [self.portlet_name, u"Popular Content portlet"]
        for e in entries:
            if e:
                return e


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('popularcontentportlet.pt')

    def update(self):
        """
        """
        pass #self.imageData = self.compileImageData()

    def get_content_by_path(self,path):
        output = None
        try:
            output = api.content.get(path)
        except Unauthorized:
            pass
        return output
            
    def popular_content(self):
        """
        Return the popular content
        """
        items_to_show = self.data.items_to_show
        url = self.data.url_of_popular_page
        black_list = self.data.black_list
        type_white_list = self.data.type_white_list
        prevent_direct_downloads = self.data.prevent_direct_downloads

        popular_urls_ = get_urls(url,black_list)

        if prevent_direct_downloads:
            popular_urls_no_downloads = []
            for p_url in popular_urls_:
                if p_url.endswith('/at_download/file'):
                    p_url = p_url.replace('at_download/file', "")
                    popular_urls_no_downloads.append(p_url)
                else:
                    popular_urls_no_downloads.append(p_url)
            popular_urls_ = popular_urls_no_downloads  

        popular_urls_remove_imagethumbs = []
        for p_url in popular_urls_:
            if p_url.endswith('/image_thumb'):
                p_url = p_url.replace('image_thumb', "")
                popular_urls_remove_imagethumbs.append(p_url)
            else:
                popular_urls_remove_imagethumbs.append(p_url)
        popular_urls_ = popular_urls_remove_imagethumbs  

        
        popular_urls__ = [(self.get_content_by_path(urlparse.urlparse(p_url).path),p_url) 
                                     for p_url in popular_urls_
                                     if self.get_content_by_path(
                                          urlparse.urlparse(p_url).path
                                          )]


        popular_urls = []
        for p_url in popular_urls__:
            if p_url[0]:
            # Check against white list while filtering out objects which
            # don't have titles
                try:
                     
                    if p_url[0].Type() in type_whitelist:
                        popular_urls.append({'title':p_url[0].Title(),
                                     'url':p_url[1]})

                except AttributeError:
                    print "bad url: %s" % p_url[1]
                
        # if needed limit by the number of items to show parameter
        if len(popular_urls) > items_to_show:
            return popular_urls[:items_to_show]
        return popular_urls

    @property
    def portlet_id(self):
        normalizer = getUtility(IIDNormalizer)
        return "portlet-popular-content-{0}".format(normalizer.normalize(
                   self.title))

    @property
    def title(self):
        return self.data.portlet_name

    def getAcquisitionChainedAssigment(self):
        """
        Apparently we need this here
        """

        # XXX: Persistently set by now by add form
        column = getattr(self.data, "column", None)
        if column:
            # column is PortletAssignmentMapping https://github.com/plone/plone.app.portlets/blob/master/plone/app/portlets/storage.py
            # which is http://svn.zope.org/zope.container/trunk/src/zope/container/ordered.py?rev=120790&view=auto
            for key, value in column.items():
                if value == self.data:
                    return column, key, column[key]

        return None



class AddForm(z3cformhelper.AddForm):

    fields = field.Fields(IPopularContentPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(z3cformhelper.EditForm):

    fields = field.Fields(IPopularContentPortlet)
