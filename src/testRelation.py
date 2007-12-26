# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testRelation.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Thu Mar  8 20:40:23 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
from relation import *

#----------------------------------------------------------------------------#

def suite():
    import relation
    testSuite = unittest.TestSuite((
            unittest.makeSuite(RelationTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class RelationTestCase(unittest.TestCase):
    """
    This class tests the Relation class. 
    """
    def setUp(self):
        self.baseSequence = [(1, 'a'), (2, 'b'), (2, 'c'), (3, 'b')]
        pass

    def testBasicOps(self):
        """
        Tests some basic construction and operations.
        """
        reln = Relation().fromSequence(self.baseSequence)
        for pair in self.baseSequence:
            assert pair in reln

        self.assertEqual(reln.forwardGet(1), set(['a']))
        self.assertEqual(reln.forwardGet(2), set(['b', 'c']))
        self.assertEqual(reln.forwardGet(3), set(['b']))

        self.assertEqual(reln.reverseGet('a'), set([1]))
        self.assertEqual(reln.reverseGet('b'), set([2, 3]))
        self.assertEqual(reln.reverseGet('c'), set([2]))

        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

