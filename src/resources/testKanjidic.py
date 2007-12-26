# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testKanjidic.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec  5 17:04:51 2006
#
#----------------------------------------------------------------------------# 

import unittest
from kanjidic import *

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(KanjidicTestCase)
        ))
    return testSuite

#----------------------------------------------------------------------------#

class KanjidicTestCase(unittest.TestCase):
    """
    This class tests the Kanjidic class. 
    """
    def setUp(self):
        self.kd = Kanjidic()
        pass

    def testLookup(self):
        """
        Tests lookup of some kanji using kanjidic.
        """
        key = u'冊'
        result = self.kd[key]
        self.assertEqual(result.strokeCount, 5)
        self.assertEqual(result.skipCode, (4, 5, 1))

        key = u'悪'
        result = self.kd[key]
        self.assertEqual(result.frequency, 469)

        return

    def testErrorCase(self):
        key = u'粉'
        assert u'こ'in self.kd[key].allReadings
        return
    
    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

