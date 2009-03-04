# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testRadkdict.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec  5 16:58:29 2006
#
#----------------------------------------------------------------------------# 

import unittest
from radkdict import *

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(RadkdictTestCase)
        ))
    return testSuite

#----------------------------------------------------------------------------#

class RadkdictTestCase(unittest.TestCase):
    """
    This class tests the Radkdict class. 
    """
    def setUp(self):
        pass

    def testConstruction(self):
        """
        Tests that the radkdict constructs itself properly.
        """
        dict = RadkDict.getCached()
        return

    def testFetchRadicals(self):
        """
        Tests fetching radicals from the radkfile. 
        """
        key = u'偏'
        dict = RadkDict.getCached()
        radicals = set(dict[key])
        expectedRadicals = set([u'一', u'｜', u'化', u'冂', u'戸', u'冊'])
        self.assertEqual(radicals, expectedRadicals)
        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

