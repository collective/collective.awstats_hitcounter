# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.awstats_hitcounter import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from collective.awstats_hitcounter.browser.utils import blacklist
from collective.awstats_hitcounter.browser.utils import type_whitelist

class ICollectiveAwstatsHitcounterLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRegistry(Interface):
    awstats_url_pattern = schema.Text(
            title=_(u"Awstats URL Path Pattern"),
            description=_(u"This needs to be an absolute url to your awstats system. Use {0} to represent the path query to be passed to awstats"),
            default=_(u"http://www.example.com/awstats/awstats.pl?urlfilter={0}&output=urldetail&config=www.example.com"),
            required=True,
    )
    url_of_popular_page = schema.TextLine(title=_(u"awstats popular content page"),
                           description=_(u"URL of the awstats page which shows popular content"),
                           required=False,
                           default=u"")

    prevent_direct_downloads = schema.Bool(title=_(u"Prevent Direct Downloads"),
                                   description=_(u"Prevent direct download of files"),
                                   default=True)
                                   
    view_more_item_count = schema.Int(title=_(u"view more item count"),
                                   description=_(u"Number of items to show on View More page"),
                                   default=150)

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
