# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.nitf.config import PROJECTNAME
from collective.nitf.testing import INTEGRATION_TESTING


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_add_permission(self):
        permission = 'collective.nitf: Add News Article'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_browserlayer_installed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INITFBrowserLayer' in layers,
                        'browser layer was not installed')

    def test_link_workflow_changed(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Link', 'obj')
        obj = self.portal['obj']
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType(obj.portal_type)
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'one_state_workflow',
                         'workflow was not changed for Link content type')

    def test_javascript_registry(self):
        portal_javascripts = self.portal.portal_javascripts
        resources = portal_javascripts.getResourceIds()
        self.assertTrue('++resource++collective.nitf/jquery.collapsible-v.2.1.3.js' in resources)
        self.assertTrue('++resource++collective.nitf/nitf_fixes.js' in resources)

    def test_css_registry(self):
        portal_css = self.portal.portal_css
        resources = portal_css.getResourceIds()
        self.assertTrue('++resource++collective.nitf/collapsible.css' in resources)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('INITFBrowserLayer' in layers,
                         'browser layer was not removed')

    def test_javascript_registry_removed(self):
        portal_javascripts = self.portal.portal_javascripts
        resources = portal_javascripts.getResourceIds()
        self.assertFalse('++resource++collective.nitf/jquery.collapsible-v.2.1.3.js' in resources)
        self.assertFalse('++resource++collective.nitf/nitf_fixes.js' in resources)

    def test_css_registry_removed(self):
        portal_css = self.portal.portal_css
        resources = portal_css.getResourceIds()
        self.assertFalse('++resource++collective.nitf/collapsible.css' in resources)
