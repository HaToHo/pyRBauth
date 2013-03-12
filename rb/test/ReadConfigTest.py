__author__ = 'Hans Hoerberg'

import unittest
import os
from rb.authorization import DeclarativeAuth


class readFileTest(unittest.TestCase):
    def testMethod(self):
        """
        Verify that the JSON file kan be read, by checking if rules, users and roles exists.
        """

        filename = os.path.dirname(os.path.abspath(__file__))+"/authSetup.json"
        #filename = os.path.dirname(os.path.abspath(__file__))+"/test.json"
        dAuth = DeclarativeAuth.getInstance(filename)

        self.assertTrue(dAuth.userExists("haho"), 'dAuth.userExists("haho") should be true')

        self.assertTrue(dAuth.ruleExists("*"), 'dAuth.ruleExists("*") should be true')

        self.assertTrue(dAuth.ruleExists("/admin"), 'dAuth.ruleExists("/admin") should be true')

        self.assertTrue(dAuth.roleExists({"admin": ["reader","writer"]}), 'dAuth.roleExists({"admin":["reader","writer"]}) should be true')

        self.assertTrue(dAuth.roleExists({"admin": ["reader"]}), 'dAuth.roleExists({"admin":["reader"]}) should be true')

        self.assertTrue(dAuth.roleExists({"admin": ["*"]}), 'dAuth.roleExists({"admin": ["*"]}) should be true')

        self.assertFalse(dAuth.roleExists({"admin": ["whatever"]}), 'dAuth.roleExists({"admin": ["whatever"]}) should be false')

if __name__ == '__main__':
    unittest.main()