# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import collective.awstats_hitcounter


class CollectiveAwstatsHitcounterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            collective.awstats_hitcounter,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.awstats_hitcounter:default')


COLLECTIVE_AWSTATS_HITCOUNTER_FIXTURE = CollectiveAwstatsHitcounterLayer()


COLLECTIVE_AWSTATS_HITCOUNTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_AWSTATS_HITCOUNTER_FIXTURE,),
    name='CollectiveAwstatsHitcounterLayer:IntegrationTesting'
)


COLLECTIVE_AWSTATS_HITCOUNTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_AWSTATS_HITCOUNTER_FIXTURE,),
    name='CollectiveAwstatsHitcounterLayer:FunctionalTesting'
)


COLLECTIVE_AWSTATS_HITCOUNTER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_AWSTATS_HITCOUNTER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveAwstatsHitcounterLayer:AcceptanceTesting'
)
