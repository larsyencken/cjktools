# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testBoolFunc.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 15:52:45 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
import boolFunc

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(BoolFuncTestCase),
            doctest.DocTestSuite(boolFunc),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class BoolFuncTestCase(unittest.TestCase):
    """ This class tests the BoolFunc class. 
    """
    def setUp(self):
        self.dataA = [1, u'dog', []]
        self.dataB = [True, u'cow', -53]
        self.dataC = [None, [], False]
        pass

    def testListMethods(self):
        u"""Tests methods which work on lists of booleans."""
        assert not boolFunc.allTrue(self.dataA)
        assert boolFunc.allTrue(self.dataB)
        assert not boolFunc.allTrue(self.dataC)

        assert boolFunc.someTrue(self.dataA)
        assert boolFunc.someTrue(self.dataB)
        assert not boolFunc.someTrue(self.dataC)

        return
    
    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

