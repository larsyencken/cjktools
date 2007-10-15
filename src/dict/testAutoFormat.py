# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testAutoFormat.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 26 11:37:59 2006
#
#----------------------------------------------------------------------------# 

import unittest
from autoFormat import *
from bilingualDict import BilingualDictionary

from settings import DATA_DIR
from os import path

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(AutoFormatTestCase)
        ))
    return testSuite

#----------------------------------------------------------------------------#

class AutoFormatTestCase(unittest.TestCase):
    """
    This class tests the AutoFormat class. 
    """
    #------------------------------------------------------------------------#

    def setUp(self):
        dictDir = path.join(DATA_DIR, 'dict')
        self.je_edict = path.join(dictDir, 'je_edict')
        self.je_jplaces = path.join(dictDir, 'je_jplaces')
        pass

    #------------------------------------------------------------------------#

    def testFormats(self):
        """
        Tests correct format detection for a variety of dictionaries.
        """
        self.assertEqual(detectFormat(self.je_edict).name, 'edict')
        self.assertEqual(detectFormat(self.je_jplaces).name, 'edict')
        return

    #------------------------------------------------------------------------#

    def testEdict(self):
        """
        Tests correct detection and parsing of edict.
        """
        dictObj = loadDictionary(self.je_edict)
        assert isinstance(dictObj, BilingualDictionary)
        self.assertEqual(dictObj.format.name, 'edict')

        self._checkLookup(dictObj,
                u'齧歯目',
                [u'げっしもく'],
                [u'(adj-no) rat-like', u'rhodential'],
            )

        self._checkLookup(dictObj,
                u'齲歯',
                [u'うし']*4 + [u'むしば']*4,
                ['(n) cavity', 'tooth decay', 'decayed tooth', 'caries']*2,
            )
        return

    #------------------------------------------------------------------------#

    def tearDown(self):
        pass

    #------------------------------------------------------------------------#

    def _checkLookup(self, dictionary, key, readings, senses):
        entry = dictionary[key]
        self.assertEqual(entry.readings, readings)
        self.assertEqual(entry.senses, senses)
        return

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:
