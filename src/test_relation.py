# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_relation.py
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
    test_suite = unittest.TestSuite((
            unittest.makeSuite(RelationTestCase),
        ))
    return test_suite

#----------------------------------------------------------------------------#

class RelationTestCase(unittest.TestCase):
    """
    This class tests the Relation class. 
    """
    def setUp(self):
        self.base_sequence = [(1, 'a'), (2, 'b'), (2, 'c'), (3, 'b')]
        pass

    def test_basic_ops(self):
        """
        Tests some basic construction and operations.
        """
        reln = Relation().from_sequence(self.base_sequence)
        for pair in self.base_sequence:
            assert pair in reln

        self.assertEqual(reln.forward_get(1), set(['a']))
        self.assertEqual(reln.forward_get(2), set(['b', 'c']))
        self.assertEqual(reln.forward_get(3), set(['b']))

        self.assertEqual(reln.reverse_get('a'), set([1]))
        self.assertEqual(reln.reverse_get('b'), set([2, 3]))
        self.assertEqual(reln.reverse_get('c'), set([2]))

        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

