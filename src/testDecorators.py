# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testDecorators.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Mar 27 13:58:57 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
from decorators import *

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(DecoratorsTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

@memoized
def getExample():
    return Example()

class Example(object):
    def __init__(self):
        self.value = 3
        return

class DecoratorsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def testMemoized(self):
        """Tests for proper caching behaviour with a simple class."""
        x = getExample()
        self.assertEqual(x.value, 3)

        y = getExample()
        assert x is y

        x.value = 5
        self.assertEqual(y.value, 5)

        return

    def testOneShot(self):
        x = [1]

        @oneShot
        def f():
            return x.pop()

        self.assertEqual(f(), 1)
        self.assertEqual(x, [])
        self.assertEqual(f(), 1)
        self.assertEqual(f(), 1)
        return
    
    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

