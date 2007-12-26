# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testPlace.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Sat Jun  9 15:09:12 2007
#
#----------------------------------------------------------------------------# 

import unittest
from place import *
import cStringIO as StringIO
import copy
import os

import warnings
warnings.simplefilter("ignore", RuntimeWarning)

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(PlaceTestCase)
        ))
    return testSuite

#----------------------------------------------------------------------------#

class PlaceTestCase(unittest.TestCase):
    """
    This class tests the Place class. 
    """
    def setUp(self):
        self.melb = Place(u'Melbourne', u'メルボルン')
        self.aust = Place(u'Australia', u'オーストラリア')
        self.filename = os.tmpnam()
        pass

    def testBasics(self):
        self.assertEqual(self.melb.label, u'Melbourne')
        self.assertEqual(self.melb.reading, u'メルボルン')

        self.aust.append(self.melb)

        assert self.melb.label in self.aust
        return

    def testFormatting(self):
        originalPlace = self.aust
        melbourne = self.melb
        melbourne.append(Place('St_Kilda', u'セーントキルダ'))
        melbourne.append(Place('Collingwood', u'コーリングウード'))
        originalPlace.append(melbourne)
        sydney = Place('Sydney', u'シドニー')
        self.assertRaises(ValueError, Place, "Anja's place")
        sydney.append(Place("Anja's_place"))
        originalPlace.append(sydney)

        originalPlace.dump(self.filename)
        newCopy = Place.fromFile(self.filename)
        self.assertEqual(newCopy, originalPlace)

    def tearDown(self):
        # Clean up the temp file we may have used.
        if os.path.exists(self.filename):
            os.remove(self.filename)
        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

