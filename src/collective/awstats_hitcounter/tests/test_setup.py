# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.awstats_hitcounter.testing import COLLECTIVE_AWSTATS_HITCOUNTER_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.awstats_hitcounter is properly installed."""

    layer = COLLECTIVE_AWSTATS_HITCOUNTER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.awstats_hitcounter is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.awstats_hitcounter'))

    def test_uninstall(self):
        """Test if collective.awstats_hitcounter is cleanly uninstalled."""
        self.installer.uninstallProducts(['collective.awstats_hitcounter'])
        self.assertFalse(self.installer.isProductInstalled('collective.awstats_hitcounter'))

    def test_browserlayer(self):
        """Test that ICollectiveAwstatsHitcounterLayer is registered."""
        from collective.awstats_hitcounter.interfaces import ICollectiveAwstatsHitcounterLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveAwstatsHitcounterLayer, utils.registered_layers())
