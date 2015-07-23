import urllib
from urlparse import urlparse
from random import shuffle
# from AccessControl import Unauthorized

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


from collective.awstats_hitcounter.browser.utils import filter_urls
from collective.awstats_hitcounter.browser.utils import get_urls
from collective.awstats_hitcounter.browser.utils import blacklist
from collective.awstats_hitcounter.browser.utils import type_whitelist

#import z3cformhelper  # XXX: Import from plone.app.portlets since Plone 4.3
import z3cformhelper


def _(x):
    """ Spoof gettext for now """
    return x


class IPopularContentPortlet(IPortletDataProvider):
    """
    Define popular content portlet fields.
    """
    portlet_name = schema.TextLine(title=_(u"Portlet Name"),
                           description=_(u"Add the name of the portlet here"),
                           required=True,
                           default=u"")

    
    read_from_the_global_registry = schema.Bool(title=_(u"Read settings from the global registry"),
                                   description=_(u"""Check this if you want to inherit from the global registry"""),
                                   default=True)

    items_to_show = schema.Int(title=_(u"Max Items to show"),
                           description=_(u"The maximum number of items that should be shown in the portlet"),
                           required=False,
                           default=3)

    url_of_popular_page = schema.TextLine(title=_(u"awstats popular content page"),
                           description=_(u"""URL of the awstats page which shows popular content 
                                           (leave blank to read from the global registry)"""),
                           required=False,
                           default=u"")

    prevent_direct_downloads = schema.Bool(title=_(u"Prevent Direct Downloads"),
                                   description=_(u"""Prevent direct download of files 
                        (if set to false, make sure it is also false in the global registry)"""),
                                   default=True)

    black_list = schema.List(title=_(u"Blacklist"),
                           description=_(u"""List of items that should not be returned as popular content
                                        (If set, this will override the global registry) 
                                         """),
                           required=False,
                           value_type=schema.TextLine(title=_(u"item")),
                           default=blacklist)

    type_white_list = schema.List(title=_(u"Type White List"),
                           description=_(u"""White list of types which should be retrieved as popular content
                                        (If set, this will override the global registry) 
                                         """),
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
    read_from_the_global_registry = FieldProperty(IPopularContentPortlet["read_from_the_global_registry"])
 

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
        Be smart about what to show as the management interface title.
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
        read_from_the_global_registry = self.data.read_from_the_global_registry

        if read_from_the_global_registry:
            url = api.portal.get_registry_record(
                            'awstats_hitcounter.url_of_popular_page')

        popular_urls = get_urls(url,black_list)

        # The following values are available via the global registry:
        # url_of_popular_page,prevent_direct_downloads
        # black_list,type_white_list
        return filter_urls(
                   popular_urls,type_white_list=type_white_list,
                   items_to_show=items_to_show,
                   prevent_direct_downloads=prevent_direct_downloads,
                   read_from_the_global_registry=read_from_the_global_registry
                    )

        

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
