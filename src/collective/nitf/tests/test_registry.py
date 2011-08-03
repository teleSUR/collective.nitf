# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry import Registry

from Products.CMFCore.utils import getToolByName

from collective.nitf import config
from collective.nitf.controlpanel import INITFSettings
from collective.nitf.testing import INTEGRATION_TESTING


class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # Set up the NITF settings registry
        self.registry = Registry()
        self.registry.registerInterface(INITFSettings)

    def test_nitf_controlpanel_view(self):
        # Test the NITF setting control panel view
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name=config.CONTROLPANEL_ID)
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_nitf_controlpanel_view_protected(self):
        # Test that the NITF setting control panel view can not be accessed
        # by anonymous users
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@nitf-settings')

    def test_nitf_in_controlpanel(self):
        # Check that there is an NITF entry in the control panel
        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.failUnless('nitf' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])

    def test_record_sections(self):
        # Test that the sections record is in the control panel
        record_sections = self.registry.records[
            'collective.nitf.controlpanel.INITFSettings.sections']
        self.failUnless('sections' in INITFSettings)
        self.assertEquals(record_sections.value, set([]))

    def test_record_default_section(self):
        # Test that the default_section record is in the control panel
        record_default_section = self.registry.records[
            'collective.nitf.controlpanel.INITFSettings.default_section']
        self.failUnless('default_section' in INITFSettings)
        self.assertEquals(record_default_section.value, None)

    def test_record_default_kind(self):
        # Test that the default_kind record is in the control panel
        record_default_kind = self.registry.records[
            'collective.nitf.controlpanel.INITFSettings.default_kind']
        self.failUnless('default_kind' in INITFSettings)
        self.assertEquals(record_default_kind.value,
                          config.DEFAULT_NEWS_TYPE)

    def test_record_default_urgency(self):
        # Test that the default_urgency record is in the control panel
        record_default_urgency = self.registry.records[
            'collective.nitf.controlpanel.INITFSettings.default_urgency']
        self.failUnless('default_urgency' in INITFSettings)
        self.assertEquals(record_default_urgency.value,
                          config.DEFAULT_URGENCY)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)