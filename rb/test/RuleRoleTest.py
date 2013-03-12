__author__ = 'Hans Hoerberg'

import unittest
import os
from rb.authorization import DeclarativeAuth
import re

class RuleRoleTest(unittest.TestCase):
    def testUserInRole(self):
        """
        Verify that users will be in correct roles.
        """

        filename = os.path.dirname(os.path.abspath(__file__))+"/authSetup.json"
        dAuth = DeclarativeAuth.getInstance(filename)

        self.assertTrue(dAuth.userInRole("haho", {"user": ["*"]}), '')
        self.assertTrue(dAuth.userInRole("haho", {"admin": ["writer"]}), '')
        self.assertTrue(dAuth.userInRole("haho", {"admin": ["reader"]}), '')
        self.assertTrue(dAuth.userInRole("haho", {"admin": ["*"]}), '')
        self.assertTrue(dAuth.userInRole("haho", {"admin": ["reader","writer"]}), '')
        self.assertTrue(dAuth.userInRole("haho", {"economics": ["writer"]}), '')
        self.assertTrue(dAuth.userInRole("haho", {"economics": ["reader"]}), '')
        self.assertTrue(dAuth.userInRole("haho", {"economics": ["*"]}), '')
        self.assertTrue(dAuth.userInRole("haho", {"economics": ["reader","writer"]}), '')

        self.assertTrue(dAuth.userInRole("test1", {"user": ["*"]}), '')
        self.assertFalse(dAuth.userInRole("test1", {"admin": ["writer"]}), '')
        self.assertFalse(dAuth.userInRole("test1", {"admin": ["reader"]}), '')
        self.assertFalse(dAuth.userInRole("test1", {"admin": ["*"]}), '')
        self.assertFalse(dAuth.userInRole("test1", {"admin": ["reader","writer"]}), '')
        self.assertFalse(dAuth.userInRole("test1", {"economics": ["writer"]}), '')
        self.assertTrue(dAuth.userInRole("test1", {"economics": ["reader"]}), '')
        self.assertTrue(dAuth.userInRole("test1", {"economics": ["*"]}), '')
        self.assertTrue(dAuth.userInRole("test1", {"economics": ["reader","writer"]}), '')

        self.assertTrue(dAuth.userInRole("test2", {"user": ["*"]}), '')
        self.assertFalse(dAuth.userInRole("test2", {"admin": ["writer"]}), '')
        self.assertFalse(dAuth.userInRole("test2", {"admin": ["reader"]}), '')
        self.assertFalse(dAuth.userInRole("test2", {"admin": ["*"]}), '')
        self.assertFalse(dAuth.userInRole("test2", {"admin": ["reader","writer"]}), '')
        self.assertTrue(dAuth.userInRole("test2", {"economics": ["writer"]}), '')
        self.assertFalse(dAuth.userInRole("test2", {"economics": ["reader"]}), '')
        self.assertTrue(dAuth.userInRole("test2", {"economics": ["*"]}), '')
        self.assertTrue(dAuth.userInRole("test2", {"economics": ["reader","writer"]}), '')

        self.assertTrue(dAuth.userInRole("test3", {"user": ["*"]}), '')
        self.assertFalse(dAuth.userInRole("test3", {"admin": ["writer"]}), '')
        self.assertTrue(dAuth.userInRole("test3", {"admin": ["reader"]}), '')
        self.assertTrue(dAuth.userInRole("test3", {"admin": ["*"]}), '')
        self.assertTrue(dAuth.userInRole("test3", {"admin": ["reader","writer"]}), '')
        self.assertTrue(dAuth.userInRole("test3", {"economics": ["writer"]}), '')
        self.assertTrue(dAuth.userInRole("test3", {"economics": ["reader"]}), '')
        self.assertTrue(dAuth.userInRole("test3", {"economics": ["*"]}), '')
        self.assertTrue(dAuth.userInRole("test3", {"economics": ["reader","writer"]}), '')


    def testUserMatchRule(self):
        """
        Verify that users can get access to protected areas, or get prevented from access areas.
        """

        filename = os.path.dirname(os.path.abspath(__file__))+"/authSetup.json"
        dAuth = DeclarativeAuth.getInstance(filename)

        self.assertFalse(dAuth.userMatchRule("/anypage","test4"), '')

        self.assertTrue(dAuth.userMatchRule("/admin/anypage","haho"), '')
        self.assertTrue(dAuth.userMatchRule("/admin","haho"), '')
        self.assertTrue(dAuth.userMatchRule("/admin/setup","haho"), '')
        self.assertTrue(dAuth.userMatchRule("/admin/setup/anypage","haho"), '')
        self.assertTrue(dAuth.userMatchRule("/economics/test.html","haho"), '')
        self.assertTrue(dAuth.userMatchRule("/economics/setup/anypage","haho"), '')
        self.assertTrue(dAuth.userMatchRule("/economics/setup/","haho"), '')
        self.assertTrue(dAuth.userMatchRule("/about","haho"), '')

        self.assertFalse(dAuth.userMatchRule("/admin/anypage","test1"), '')
        self.assertFalse(dAuth.userMatchRule("/admin","test1"), '')
        self.assertFalse(dAuth.userMatchRule("/admin/setup","test1"), '')
        self.assertFalse(dAuth.userMatchRule("/admin/setup/anypage","test1"), '')
        self.assertTrue(dAuth.userMatchRule("/economics/test.html","test1"), '')
        self.assertFalse(dAuth.userMatchRule("/economics/setup/anypage","test1"), '')
        self.assertFalse(dAuth.userMatchRule("/economics/setup/","test1"), '')
        self.assertTrue(dAuth.userMatchRule("/about","test1"), '')


if __name__ == '__main__':
    unittest.main()


