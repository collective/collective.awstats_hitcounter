# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.awstats_hitcounter import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveAwstatsHitcounterLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IRegistry(Interface):
    awstats_url_pattern = schema.Text(
            title=_(u"Awstats URL Path Pattern"),
            description=_(u"This needs to be an absolute url to your awstats system. Use {} to represent the path query to be passed to awstats"),
            default=_(u"http://www.example.com/awstats/awstats.pl?urlfilter={}&output=urldetail&config=www.example.com"),
            required=True,
    )
