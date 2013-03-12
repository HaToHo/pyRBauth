__author__ = 'Hans Hoerberg'

import unittest
from rb.authorization import DeclarativeAuth


class singletonTest(unittest.TestCase):
    def testMethod(self):
        """
        Verify that the singleton works
        """
        self.assertEqual(DeclarativeAuth.getInstance().classId(), DeclarativeAuth.getInstance().classId(),
                         'DeclarativeAuth.getInstance().classId() = DeclarativeAuth.getInstance().classId()')


if __name__ == '__main__':
    unittest.main()