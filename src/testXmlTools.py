# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testXml.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Oct 16 13:00:29 2006
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
import os
from xmlTools import *

#----------------------------------------------------------------------------#

_dirName = os.path.abspath(os.path.dirname(__file__))

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(IndexTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class IndexTestCase(unittest.TestCase):
    """
    This class tests the Index class. 
    """
    #------------------------------------------------------------------------#

    def setUp(self):
        global _dirName
        self.sampleFile = os.path.join(_dirName, 'sampleDoc.xml')
        self.indexFile = os.path.join(_dirName, 'sampleDoc.xml.index')

        if os.path.exists(self.indexFile):
            os.remove(self.indexFile)

        return

    #------------------------------------------------------------------------#

    def testIndexingByElement(self):
        """
        Checks for correct keys and values, indexing by elements.
        """
        doc = IndexedDocument(self.sampleFile, 'targetElement', 'name')
        assert os.path.exists(self.indexFile)
        self.assertEquals(set(doc.keys()), set(('Mary', 'This little piggy')))

        maryDoc = doc['Mary']
        self.assertEquals(EvaluateLeaf('targetElement/had', maryDoc),
                'a little lamb')

        piggyDoc = doc['This little piggy']
        self.assertEquals(EvaluateLeaf('targetElement/had', piggyDoc),
                'roast beef')

        return

    #------------------------------------------------------------------------#

    def testIndexingByAttribute(self):
        """
        Checks for correct keys and values, indexing by attributes.
        """
        doc = IndexedDocument(self.sampleFile, 'targetElement', '@realname')

        self.assertEquals(set(doc.keys()), set(('Shiela', 'Frank')))

        maryDoc = doc['Shiela']
        self.assertEquals(EvaluateLeaf('targetElement/had', maryDoc),
                'a little lamb')

        piggyDoc = doc['Frank']
        self.assertEquals(EvaluateLeaf('targetElement/had', piggyDoc),
                'roast beef')

        return

    #------------------------------------------------------------------------#

    def tearDown(self):
        if os.path.exists(self.indexFile):
            os.remove(self.indexFile)

        return

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

