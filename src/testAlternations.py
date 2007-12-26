# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testAlternations.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Thu Jun 28 15:59:34 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
import alternations
import stats

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(AlternationsTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class AlternationsTestCase(unittest.TestCase):
    """
    This class tests the Alternations class. 
    """
    def setUp(self):
        pass

    def testCanonicalForms(self):
        base = (u'ゆっ', u'ぐり')
        seg1Cases = [u'ゆ' + c for c in u'いちりきつくっ']
        seg2Cases = [u'くり', u'ぐり']
        expected = set(stats.combinations([seg1Cases, seg2Cases]))

        self.assertEqual(set(alternations.canonicalForms(base)), expected)

    def testCanonicalSegmentForms(self):
        voiced = u'ばり'
        expected = set([u'ばり', u'はり'])
        result = set(alternations.canonicalSegmentForms(voiced, True, False))
        self.assertEqual(result, expected)

        self.assertEqual(alternations.canonicalSegmentForms(u'わ'),
                set([u'わ']))

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:
